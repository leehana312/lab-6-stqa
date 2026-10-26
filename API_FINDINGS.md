# API Findings: JSONPlaceholder

Testers (Group 5): Elisa, Nurfarhana, Ammar, Ikmal, Shervona, Nureen
Date: 26 October 2026

Record what the server actually returned for each route. A value
copied from the documentation without being checked against a real
request is not a finding.

## GET /posts/1

| Field        | Value                           |
| ------------ | ------------------------------- |
| Status code  | 200                             |
| Content-Type | application/json; charset=utf-8 |

Response body keys and their types:

| Key    | Type | Example value                                                                |
| ------ | ---- | ---------------------------------------------------------------------------- |
| userId | int  | 1                                                                            |
| id     | int  | 1                                                                            |
| title  | str  | "sunt aut facere repellat provident occaecati excepturi optio reprehenderit" |
| body   | str  | "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum..."      |

## GET /posts

| Field        | Value                           |
| ------------ | ------------------------------- |
| Status code  | 200                             |
| Content-Type | application/json; charset=utf-8 |

Shape of the response body (object or array, and the type of each
element):

A JSON array of 100 elements. Each element is an object with the same
four keys as GET /posts/1: `userId` (int), `id` (int), `title` (str),
`body` (str). The first element is post id 1.

## POST /posts

Request body sent:

```json
{
  "title": "foo",
  "body": "bar",
  "userId": 1
}
```

| Field        | Value                           |
| ------------ | ------------------------------- |
| Status code  | 201                             |
| Content-Type | application/json; charset=utf-8 |

Response body keys and their types:

| Key    | Type | Example value             |
| ------ | ---- | ------------------------- |
| title  | str  | "foo"                     |
| body   | str  | "bar"                     |
| userId | int  | 1                         |
| id     | int  | 101 (added by the server) |

## DELETE /posts/1

| Field        | Value                           |
| ------------ | ------------------------------- |
| Status code  | 200                             |
| Content-Type | application/json; charset=utf-8 |

Response body:

`{}` (an empty JSON object)

## Notes

- Content-Type for every route is `application/json; charset=utf-8`,
  not plain `application/json` as used in Part 1. Tests must assert
  the full value or they will fail.
- POST /posts returned 201 and a new id (101), but a follow-up
  GET /posts/101 returned 404. The post was never actually saved.
- DELETE /posts/1 returned 200, but a follow-up GET /posts/1 still
  returned 200. The post was never actually deleted.
- Conclusion: JSONPlaceholder accepts POST and DELETE and returns
  success codes, but does not change any data on the server. A test
  that checks only the status code would wrongly pass. Confirming a
  write requires reading the resource back afterwards.
