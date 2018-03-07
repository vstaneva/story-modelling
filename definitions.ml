type distribution =
  Uniform  of float*float (* low, high *)
| DUniform of int*int     (* low, high *)
| Coin     of float       (* prob of heads *)

type arrow = Arrow of string*float (* label, probability *)
type layer =
  { name    : string
  ; process : distribution
  ; data    : 'a list
  }

type t = {
}