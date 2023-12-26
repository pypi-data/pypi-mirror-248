use core::ops::ControlFlow;
use sqlparser::ast::{
    Expr, OrderByExpr, Query, SelectItem, SetExpr, Statement, Value, VisitMut, VisitorMut,
};
use sqlparser::dialect::AnsiDialect;
use sqlparser::parser::Parser;

use pyo3::prelude::*;

struct Formalizer {
    broken: bool,
}

impl Formalizer {
    pub fn is_broken(&self) -> bool {
        self.broken
    }
}

fn construct_order_by(count: usize) -> Vec<OrderByExpr> {
    let mut v = Vec::new();
    for i in 1..count + 1 {
        let number = Value::Number(i.to_string(), false);
        let expr = Expr::Value(number);
        v.push(OrderByExpr {
            expr,
            asc: None,
            nulls_first: None,
        });
    }
    v
}

fn no_wild(projection: &Vec<SelectItem>) -> bool {
    for project in projection {
        match project {
            SelectItem::QualifiedWildcard(_, _) => {
                return false;
            }
            SelectItem::Wildcard(_) => {
                return false;
            }
            _ => {}
        }
    }
    true
}

fn need_to_add_limit(limit: &Option<Expr>) -> bool {
    match limit {
        Some(limit) => match limit {
            Expr::Value(value) => match value {
                Value::Number(val, _) => {
                    let parsed: Result<u32, _> = val.parse();
                    match &parsed {
                        Ok(val) => {
                            if val <= &20000 {
                                false
                            } else {
                                true
                            }
                        }
                        Err(_) => true,
                    }
                }
                _ => true,
            },
            _ => true,
        },
        _ => true,
    }
}

impl VisitorMut for Formalizer {
    type Break = ();

    fn pre_visit_query(&mut self, query: &mut Query) -> ControlFlow<Self::Break> {
        let body = query.body.as_ref();
        match body {
            SetExpr::Select(select) => {
                if !no_wild(&select.projection) {
                    self.broken = true;
                    return ControlFlow::Break(());
                }
                query.order_by = construct_order_by(select.projection.len());
                if need_to_add_limit(&query.limit) {
                    query.limit = Some(Expr::Value(Value::Number(String::from("20000"), false)));
                }
                query.limit_by = vec![];
                ControlFlow::Continue(())
            }
            SetExpr::SetOperation {
                left,
                op: _,
                set_quantifier: _,
                right: _,
            } => match left.as_ref() {
                SetExpr::Select(select) => {
                    if !no_wild(&select.projection) {
                        self.broken = true;
                        return ControlFlow::Break(());
                    }
                    query.order_by = construct_order_by(select.projection.len());
                    if need_to_add_limit(&query.limit) {
                        query.limit =
                            Some(Expr::Value(Value::Number(String::from("20000"), false)));
                    }
                    query.limit_by = vec![];
                    ControlFlow::Continue(())
                }
                _ => ControlFlow::Continue(()),
            },
            _ => ControlFlow::Continue(()),
        }
    }
}

fn make_deterministic(sql: &str) -> String {
    let result = Parser::parse_sql(&AnsiDialect {}, sql);
    match result {
        Ok(mut statements) => {
            if statements.len() == 0 {
                "".to_owned()
            } else {
                let mut first_statement = &mut statements[0];
                make_deterministic_impl(&mut first_statement)
            }
        }
        Err(_) => "".to_owned(),
    }
}

fn make_deterministic_impl(statement: &mut Statement) -> String {
    let mut visitor = Formalizer { broken: false };
    statement.visit(&mut visitor);
    if visitor.is_broken() {
        String::from("")
    } else {
        statement.to_string()
    }
}

#[pyfunction]
#[pyo3(text_signature = "(sql)")]
#[pyo3(name = "make_deterministic")]
fn python_wrapper(sql: &str) -> PyResult<String> {
    Ok(make_deterministic(sql))
}

#[pymodule]
fn deterministic_sql(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(python_wrapper, m)?)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use crate::make_deterministic;

    #[test]
    fn simple() {
        let sql = "select a, b, c from t";
        assert_eq!(
            make_deterministic(sql),
            "SELECT a, b, c FROM t ORDER BY 1, 2, 3 LIMIT 20000"
        );
    }

    #[test]
    fn nested() {
        let sql = "select a, b, c from (select a, b, c from t)";
        assert_eq!(
            make_deterministic(sql),
            "SELECT a, b, c FROM (SELECT a, b, c FROM t ORDER BY 1, 2, 3 LIMIT 20000) ORDER BY 1, 2, 3 LIMIT 20000"
        );
    }

    #[test]
    fn limit() {
        let sql = "select a, b, c from t limit 10";
        assert_eq!(
            make_deterministic(sql),
            "SELECT a, b, c FROM t ORDER BY 1, 2, 3 LIMIT 10"
        );
    }

    #[test]
    fn wild() {
        let sql = "select * from t limit 10";
        assert_eq!(make_deterministic(sql), "");
    }

    #[test]
    fn union() {
        let sql = "select a from t1 union all select b from t2";
        assert_eq!(
            make_deterministic(sql),
            "SELECT a FROM t1 UNION ALL SELECT b FROM t2 ORDER BY 1 LIMIT 20000"
        );
    }

    #[test]
    fn join() {
        let sql = "
            SELECT orders.order_id, orders.order_amount, customers.customer_name
            FROM orders
            INNER JOIN (
                SELECT customer_id, customer_name
                FROM customers
            ) AS customers ON orders.customer_id = customers.customer_id;";
        assert_eq!(
            make_deterministic(sql),
            "SELECT orders.order_id, orders.order_amount, customers.customer_name FROM orders JOIN (SELECT customer_id, customer_name FROM customers ORDER BY 1, 2 LIMIT 20000) AS customers ON orders.customer_id = customers.customer_id ORDER BY 1, 2, 3 LIMIT 20000"
        );
    }
}
