#ifndef __SUNFISH_HPP
#define __SUNFISH_HPP

using namespace __shedskin__;
namespace __sunfish__ {

extern str *const_0, *const_1, *const_10, *const_11, *const_12, *const_13, *const_14, *const_15, *const_16, *const_17, *const_18, *const_19, *const_2, *const_20, *const_21, *const_22, *const_23, *const_24, *const_25, *const_26, *const_27, *const_28, *const_29, *const_3, *const_30, *const_31, *const_32, *const_33, *const_34, *const_35, *const_36, *const_37, *const_38, *const_39, *const_4, *const_5, *const_6, *const_7, *const_8, *const_9;

class Position;
class Entry;
class Searcher;

typedef tuple<__ss_int> *(*lambda0)(tuple<__ss_int> *);
typedef str *(*lambda1)(str *, __ss_int, str *);
typedef __ss_bool (*lambda2)(Position *);

extern str *__name__, *initial, *k;
extern __ss_int A1, A8, E, EVAL_ROUGHNESS, H1, H8, MATE_LOWER, MATE_UPPER, N, QS_LIMIT, S, W, __15, __16, __3, movecount;
extern dict<str *, __ss_int> *piece;
extern dict<str *, tuple<__ss_int> *> *directions, *pst;
extern tuple<__ss_int> *table;
extern lambda0 padrow;
extern void *i, *x;
extern list<list<tuple<__ss_int> *> *> *movecache;
extern __ss_float TABLE_SIZE;
extern __ss_bool DRAW_TEST;
extern tuple2<str *, tuple<__ss_int> *> *__0;
extern list<tuple2<str *, tuple<__ss_int> *> *> *__1;
extern __iter<tuple2<str *, tuple<__ss_int> *> *> *__2;


extern class_ *cl_Position;
class Position : public pyobj {
/**
A state of a chess game
board -- a 120 char representation of the board
score -- the board evaluation
wc -- the castling rights, [west/queen side, east/king side]
bc -- the opponent castling rights, [west/king side, east/queen side]
ep - the en passant square
kp - the king passant square
*/
public:
    __ss_int kp;
    str *board;
    __ss_int ep;
    tuple<__ss_bool> *bc;
    tuple<__ss_bool> *wc;
    __ss_int score;

    Position() {}
    Position(str *board, __ss_int score, tuple<__ss_bool> *wc, tuple<__ss_bool> *bc, __ss_int ep, __ss_int kp) {
        this->__class__ = cl_Position;
        __init__(board, score, wc, bc, ep, kp);
    }
    static void __static__();
    void *__init__(str *board, __ss_int score, tuple<__ss_bool> *wc, tuple<__ss_bool> *bc, __ss_int ep, __ss_int kp);
    __ss_bool __eq__(Position *other);
    long __hash__();
    __iter<tuple<__ss_int> *> *gen_moves();
    Position *rotate();
    Position *nullmove();
    Position *move(tuple<__ss_int> *move);
    __ss_int value(tuple<__ss_int> *move);
};

extern class_ *cl_Entry;
class Entry : public pyobj {
public:
    __ss_int lower;
    __ss_int upper;

    Entry() {}
    Entry(__ss_int lower, __ss_int upper) {
        this->__class__ = cl_Entry;
        __init__(lower, upper);
    }
    void *__init__(__ss_int lower, __ss_int upper);
};

extern class_ *cl_Searcher;
class Searcher : public pyobj {
public:
    dict<tuple2<Position *, tuple2<__ss_int, __ss_bool> *> *, Entry *> *tp_score;
    __ss_int nodes;
    set<Position *> *history;
    dict<Position *, tuple<__ss_int> *> *tp_move;

    Searcher() {}
    Searcher(int __ss_init) {
        this->__class__ = cl_Searcher;
        __init__();
    }
    void *__init__();
    __iter<tuple2<tuple<__ss_int> *, __ss_int> *> *moves(__ss_int depth, __ss_bool root, Position *pos, __ss_int gamma);
    __ss_int bound(Position *pos, __ss_int gamma, __ss_int depth, __ss_bool root);
    __iter<tuple2<__ss_int, tuple2<tuple<__ss_int> *, __ss_int> *> *> *search(Position *pos, list<Position *> *history);
};

extern __ss_bool  default_0;
extern list<Position *> * default_1;
__ss_int parse(str *c);
str *render(__ss_int i);
void *print_pos(Position *pos);
void *__ss_main();

} // module namespace
namespace __shedskin__ { /* XXX */
template<> inline __ss_int __cmp(__sunfish__::Position *a, __sunfish__::Position *b) {
    if (!a) return -1;
    if(a->__eq__(b)) return 0;
    return __cmp<void *>(a, b);
}
}
#endif
