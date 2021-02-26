initial_state( b(0,0) ).
end_state( b(2,0) ).

trans ( b(X,Y), b(4,Y) ) :- X<4.
trans ( b(X,Y), b(X,3) ) :- Y<3.
trans ( b(X,Y), b(0,Y) ) :- X>0.
trans ( b(X,Y), b(X,0) ) :- Y>0.

trans ( b(X,Y), b(4,Y1) ) :-
        X+Y>=4,
        X<4,
        Y1 is Y-(4-X).

trans ( b(X,Y), b(X1,3) ) :-
        X+Y>=3,
        Y<3,
        X1 is X-(3-Y).

trans ( b(X,Y), b(X1,0) ) :-
        X+Y<4,
        Y>0,
        X1 is X+Y.

trans ( b(X,Y), b(0,Y1) ) :-
        X+Y<3,
        X>0,
        Y1 is X+Y.