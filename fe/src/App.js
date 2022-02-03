import logo from "./logo.svg";
import "./App.css";
import React, { useState } from "react";

import { Button, Form, Row, Col, Card, ListGroup } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.css";

async function getSearchApi(params) {
  return fetch(`/search?q=${params}`, {
    headers: {
      "Content-Type": "application/json",
    },
    method: "GET",
  }).then((data) => data.json());
}

function App() {
  const [search, setSearch] = useState("");
  const [result, setResult] = useState([]);

  const handleSearch = async (e) => {
    //to remove
    setResult([
      {
        name: "file1",
        link: "www.google.com",
      },
      {
        name: "file2",
        link: "www.google.com",
      },
    ]);

    getSearchApi(search).then((data) => {
      console.log(data);

      setResult(data);

      //set data here
    });
  };

  const onResult = () => {
    if (result.length > 0) {
      return (
        <div>
          <Row className="justify-content-md-center">
            <Col xs={5}>
              <Card>
                <Card.Header as="h5" style={{ textAlign: "center" }}>
                  Result
                </Card.Header>
                <br></br>
                {result.map((item, index) => (
                  <Row className="justify-content-md-center" key={index}>
                    <Col xs={8}>
                      <ListGroup as="ol">
                        <ListGroup.Item
                          as="li"
                          className="d-flex justify-content-between align-items-start"
                        >
                          {index + 1}.{item.name}{" "}
                          <Card.Link href={"http://" + item.link}>
                            {item.link.length < 23
                              ? `${item.link}`
                              : `${item.link.substring(0, 20)}...`}{" "}
                          </Card.Link>
                        </ListGroup.Item>
                      </ListGroup>
                    </Col>
                  </Row>
                ))}
                <br></br>
              </Card>
            </Col>
          </Row>
        </div>
      );
    }
  };

  return (
    <div className="App">
      <br></br>
      <Row className="justify-content-md-center">
        <Col xs={5}>
          <Card>
            <Card.Header as="h5" style={{ textAlign: "center" }}>
              Search
            </Card.Header>
            <br></br>
            <Row className="justify-content-md-center">
              <Col xs={8}>
                <Form>
                  <Form.Group className="mb-3">
                    <Form.Control
                      placeholder="Enter Search"
                      onChange={(e) => setSearch(e.target.value)}
                    />
                  </Form.Group>
                </Form>
              </Col>
              <Col xs={1}>
                <Button variant="primary" type="submit" onClick={handleSearch}>
                  Search
                </Button>
              </Col>
            </Row>

            <br></br>
          </Card>
        </Col>
      </Row>
      <br></br>
      {onResult()}
    </div>
  );
}

export default App;
