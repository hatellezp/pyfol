%------------------------------------------------------------------------------
% File     : AGT001+0 : TPTP v8.2.0. Released v2.7.0.
% Domain   : Agents
% Axioms   : CPlanT system
% Version  : [Bar03] axioms : Especial.
% English  :

% Refs     : [Bar03] Barta, J. (2003), Email to G. Sutcliffe
% Source   : [Bar03]
% Names    :

% Status   : Satisfiable
% Syntax   : Number of formulae    :   20 (   0 unt;   0 def)
%            Number of atoms       :   98 (   0 equ)
%            Maximal formula atoms :    6 (   4 avg)
%            Number of connectives :   79 (   1   ~;   0   |;  58   &)
%                                         (  14 <=>;   6  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    8 (   7 avg)
%            Maximal term depth    :    1 (   1 avg)
%            Number of predicates  :   10 (  10 usr;   0 prp; 2-4 aty)
%            Number of functors    :   47 (  47 usr;  47 con; 0-0 aty)
%            Number of variables   :   35 (  35   !;   0   ?)
% SPC      :

% Comments : Requires NUM005+0.ax NUM005+1.ax
%------------------------------------------------------------------------------
fof(a1_1,axiom,
    ? [A,C,N,L] :
      ( accept_team(a,L,C,N)
    <=> ( accept_city(A,C)
        & accept_leader(A,L)
        & accept_number(A,N) ) ) ).

