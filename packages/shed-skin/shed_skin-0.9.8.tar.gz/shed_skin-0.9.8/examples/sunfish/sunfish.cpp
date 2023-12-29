#include "builtin.hpp"
#include "itertools.hpp"
#include "time.hpp"
#include "re.hpp"
#include "sunfish.hpp"

namespace __sunfish__ {

str *const_0, *const_1, *const_10, *const_11, *const_12, *const_13, *const_14, *const_15, *const_16, *const_17, *const_18, *const_19, *const_2, *const_20, *const_21, *const_22, *const_23, *const_24, *const_25, *const_26, *const_27, *const_28, *const_29, *const_3, *const_30, *const_31, *const_32, *const_33, *const_34, *const_35, *const_36, *const_37, *const_38, *const_39, *const_4, *const_5, *const_6, *const_7, *const_8, *const_9;

using __itertools__::count;

str *__name__, *initial, *k;
__ss_int A1, A8, E, EVAL_ROUGHNESS, H1, H8, MATE_LOWER, MATE_UPPER, N, QS_LIMIT, S, W, __15, __16, __3, movecount;
dict<str *, __ss_int> *piece;
dict<str *, tuple<__ss_int> *> *directions, *pst;
tuple<__ss_int> *table;
lambda0 padrow;
void *i, *x;
list<list<tuple<__ss_int> *> *> *movecache;
__ss_float TABLE_SIZE;
__ss_bool DRAW_TEST;
tuple2<str *, tuple<__ss_int> *> *__0;
list<tuple2<str *, tuple<__ss_int> *> *> *__1;
__iter<tuple2<str *, tuple<__ss_int> *> *> *__2;
list<tuple2<str *, tuple<__ss_int> *> *>::for_in_loop __4;


__ss_bool  default_0;
list<Position *> * default_1;
class list_comp_0 : public __iter<__ss_int> {
public:
    __ss_int __7, x;
    tuple<__ss_int> *__5;
    __iter<__ss_int> *__6;
    tuple<__ss_int>::for_in_loop __8;

    tuple<__ss_int> *row;
    int __last_yield;

    list_comp_0(tuple<__ss_int> *row);
    __ss_int __get_next();
};

class list_comp_1 : public __iter<tuple<__ss_int> *> {
public:
    __ss_int __10, __9, i;

    int __last_yield;

    list_comp_1();
    tuple<__ss_int> * __get_next();
};

static inline list<tuple<__ss_int> *> *list_comp_2(__ss_int i);
static inline list<list<tuple<__ss_int> *> *> *list_comp_3();
class list_comp_4 : public __iter<__ss_bool> {
public:
    str *__68, *c;
    __iter<str *> *__69;
    __ss_int __70;
    str::for_in_loop __71;

    Position *pos;
    int __last_yield;

    list_comp_4(Position *pos);
    __ss_bool __get_next();
};

static inline list<tuple2<__ss_int, tuple<__ss_int> *> *> *list_comp_5(Position *pos);
class list_comp_6 : public __iter<__ss_bool> {
public:
    tuple<__ss_int> *m;
    __iter<tuple<__ss_int> *> *__107, *__108;
    __ss_int __109;
    __iter<tuple<__ss_int> *>::for_in_loop __110;
    void *__111;
    Position *__112;

    Position *pos;
    int __last_yield;

    list_comp_6(Position *pos);
    __ss_bool __get_next();
};

class list_comp_7 : public __iter<__ss_bool> {
public:
    tuple<__ss_int> *m;
    __iter<tuple<__ss_int> *> *__113, *__114;
    __ss_int __115;
    __iter<tuple<__ss_int> *>::for_in_loop __116;
    void *__117;
    Position *__118;

    lambda2 is_dead;
    Position *pos;
    int __last_yield;

    list_comp_7(lambda2 is_dead, Position *pos);
    __ss_bool __get_next();
};

class list_comp_8 : public __iter<str *> {
public:
    str *__134, *p;
    __iter<str *> *__135;
    __ss_int __136;
    str::for_in_loop __137;

    str *row;
    dict<str *, str *> *uni_pieces;
    int __last_yield;

    list_comp_8(str *row, dict<str *, str *> *uni_pieces);
    str * __get_next();
};

static inline tuple<__ss_int> *__lambda0__(tuple<__ss_int> *row);
static inline str *__lambda1__(str *board, __ss_int i, str *p);
static inline __ss_bool __lambda2__(Position *pos);

list_comp_0::list_comp_0(tuple<__ss_int> *row) {
    this->row = row;
    __last_yield = -1;
}

__ss_int list_comp_0::__get_next() {
    if(!__last_yield) goto __after_yield_0;
    __last_yield = 0;

    FOR_IN(x,row,5,7,8)
        __result = (x+__sunfish__::piece->__getitem__(__sunfish__::k));
        return __result;
        __after_yield_0:;
    END_FOR

    __stop_iteration = true;
    return __zero<__ss_int>();
}

list_comp_1::list_comp_1() {
    __last_yield = -1;
}

tuple<__ss_int> * list_comp_1::__get_next() {
    if(!__last_yield) goto __after_yield_0;
    __last_yield = 0;

    FAST_FOR(i,0,__ss_int(8),1,9,10)
        __result = __sunfish__::padrow(__sunfish__::table->__slice__(__ss_int(3), (i*__ss_int(8)), ((i*__ss_int(8))+__ss_int(8)), __ss_int(0)));
        return __result;
        __after_yield_0:;
    END_FOR

    __stop_iteration = true;
    return __zero<tuple<__ss_int> *>();
}

static inline list<tuple<__ss_int> *> *list_comp_2(__ss_int i) {
    __ss_int __13, __14, j;

    list<tuple<__ss_int> *> *__ss_result = new list<tuple<__ss_int> *>();

    FAST_FOR(j,0,__ss_int(120),1,13,14)
        __ss_result->append((new tuple<__ss_int>(2,i,j)));
    END_FOR

    return __ss_result;
}

static inline list<list<tuple<__ss_int> *> *> *list_comp_3() {
    __ss_int __11, __12, i;

    list<list<tuple<__ss_int> *> *> *__ss_result = new list<list<tuple<__ss_int> *> *>();

    FAST_FOR(i,0,__ss_int(120),1,11,12)
        __ss_result->append(list_comp_2(i));
    END_FOR

    return __ss_result;
}

list_comp_4::list_comp_4(Position *pos) {
    this->pos = pos;
    __last_yield = -1;
}

__ss_bool list_comp_4::__get_next() {
    if(!__last_yield) goto __after_yield_0;
    __last_yield = 0;

    __68 = const_0;
    FOR_IN(c,__68,68,70,71)
        __result = ___bool((pos->board)->__contains__(c));
        return __result;
        __after_yield_0:;
    END_FOR

    __stop_iteration = true;
    return __zero<__ss_bool>();
}

static inline list<tuple2<__ss_int, tuple<__ss_int> *> *> *list_comp_5(Position *pos) {
    tuple<__ss_int> *move;
    __iter<tuple<__ss_int> *> *__77, *__78;
    __ss_int __79;
    __iter<tuple<__ss_int> *>::for_in_loop __80;
    void *__81;
    Position *__82;

    list<tuple2<__ss_int, tuple<__ss_int> *> *> *__ss_result = new list<tuple2<__ss_int, tuple<__ss_int> *> *>();

    __77 = pos->gen_moves();
    FOR_IN(move,__77,77,79,80)
        __ss_result->append((new tuple2<__ss_int, tuple<__ss_int> *>(2,pos->value(move),move)));
    END_FOR

    return __ss_result;
}

list_comp_6::list_comp_6(Position *pos) {
    this->pos = pos;
    __last_yield = -1;
}

__ss_bool list_comp_6::__get_next() {
    if(!__last_yield) goto __after_yield_0;
    __last_yield = 0;

    __107 = pos->gen_moves();
    FOR_IN(m,__107,107,109,110)
        __result = ___bool((pos->value(m)>=__sunfish__::MATE_LOWER));
        return __result;
        __after_yield_0:;
    END_FOR

    __stop_iteration = true;
    return __zero<__ss_bool>();
}

list_comp_7::list_comp_7(lambda2 is_dead, Position *pos) {
    this->is_dead = is_dead;
    this->pos = pos;
    __last_yield = -1;
}

__ss_bool list_comp_7::__get_next() {
    if(!__last_yield) goto __after_yield_0;
    __last_yield = 0;

    __113 = pos->gen_moves();
    FOR_IN(m,__113,113,115,116)
        __result = is_dead(pos->move(m));
        return __result;
        __after_yield_0:;
    END_FOR

    __stop_iteration = true;
    return __zero<__ss_bool>();
}

list_comp_8::list_comp_8(str *row, dict<str *, str *> *uni_pieces) {
    this->row = row;
    this->uni_pieces = uni_pieces;
    __last_yield = -1;
}

str * list_comp_8::__get_next() {
    if(!__last_yield) goto __after_yield_0;
    __last_yield = 0;

    FOR_IN(p,row,134,136,137)
        __result = uni_pieces->get(p, p);
        return __result;
        __after_yield_0:;
    END_FOR

    __stop_iteration = true;
    return __zero<str *>();
}

static inline tuple<__ss_int> *__lambda0__(tuple<__ss_int> *row) {
    
    return (((new tuple<__ss_int>(1,__ss_int(0))))->__add__((new tuple<__ss_int>(new list_comp_0(row)))))->__add__((new tuple<__ss_int>(1,__ss_int(0))));
}

static inline str *__lambda1__(str *board, __ss_int i, str *p) {
    
    return __add_strs(3, board->__slice__(__ss_int(2), __ss_int(0), i, __ss_int(0)), p, board->__slice__(__ss_int(1), (i+__ss_int(1)), __ss_int(0), __ss_int(0)));
}

static inline __ss_bool __lambda2__(Position *pos) {
    
    return any(new list_comp_6(pos));
}

/**
class Position
*/

class_ *cl_Position;

void *Position::__init__(str *board, __ss_int score, tuple<__ss_bool> *wc, tuple<__ss_bool> *bc, __ss_int ep, __ss_int kp) {
    
    this->board = board;
    this->score = score;
    this->wc = wc;
    this->bc = bc;
    this->ep = ep;
    this->kp = kp;
    return NULL;
}

__ss_bool Position::__eq__(Position *other) {
    __ss_bool __17, __18, __19, __20, __21, __22;

    return __AND(___bool(__eq(this->board, other->board)), __AND(___bool((this->score==other->score)), __AND(___bool(__eq(this->wc, other->wc)), __AND(___bool(__eq(this->bc, other->bc)), __AND(___bool((this->ep==other->ep)), ___bool((this->kp==other->kp)), 21), 20), 19), 18), 17);
}

long Position::__hash__() {
    
    return (((((hasher(this->board)+hasher(this->score))+hasher(this->wc))+hasher(this->bc))+hasher(this->ep))+hasher(this->kp));
}

class __gen_Position_gen_moves : public __iter<tuple<__ss_int> *> {
public:
    __ss_int __26, __31, __35, d, i, j;
    str *__27, *p, *q;
    Position *self;
    tuple2<__ss_int, str *> *__23;
    __iter<tuple2<__ss_int, str *> *> *__24, *__25;
    __iter<tuple2<__ss_int, str *> *>::for_in_loop __28;
    tuple<__ss_int> *__29;
    __iter<__ss_int> *__30, *__33, *__34;
    tuple<__ss_int>::for_in_loop __32;
    __iter<__ss_int>::for_in_loop __36;
    __ss_bool __37, __38, __39, __40, __41, __42, __43, __44, __45, __46, __47, __48, __49, __50, __51, __52, __53, __54, __55;

    int __last_yield;

    __gen_Position_gen_moves(Position *self) {
        this->self = self;
        __last_yield = -1;
    }

    tuple<__ss_int> * __get_next() {
        switch(__last_yield) {
            case 0: goto __after_yield_0;
            case 1: goto __after_yield_1;
            case 2: goto __after_yield_2;
            default: break;
        }

        FOR_IN_ENUMERATE_STR(p,self->board,27,26)
            i = __26;
            if (__NOT(p->isupper())) {
                continue;
            }

            FOR_IN(d,__sunfish__::directions->__getitem__(p),29,31,32)

                FOR_IN(j,count((i+d), d),33,35,36)
                    q = (self->board)->__getfast__(j);
                    if ((q->isspace() or q->isupper())) {
                        break;
                    }
                    if (__eq(p, const_1)) {
                        if (((__eq(d,__sunfish__::N) | __eq(d,(__sunfish__::N+__sunfish__::N))) and __ne(q, const_2))) {
                            break;
                        }
                        if (((d==(__sunfish__::N+__sunfish__::N)) and ((i<(__sunfish__::A1+__sunfish__::N)) or __ne((self->board)->__getfast__((i+__sunfish__::N)), const_2)))) {
                            break;
                        }
                        if (((__eq(d,(__sunfish__::N+__sunfish__::W)) | __eq(d,(__sunfish__::N+__sunfish__::E))) and __eq(q, const_2) and (!__eq(j,self->ep) && !__eq(j,self->kp) && !__eq(j,(self->kp-__ss_int(1))) && !__eq(j,(self->kp+__ss_int(1)))))) {
                            break;
                        }
                    }
                    __last_yield = 0;
                    __result = (__sunfish__::movecache->__getfast__(i))->__getfast__(j);
                    return __result;
                    __after_yield_0:;
                    if (((const_3)->__contains__(p) or q->islower())) {
                        break;
                    }
                    if (((i==__sunfish__::A1) and __eq((self->board)->__getfast__((j+__sunfish__::E)), const_4) and self->wc->__getfirst__())) {
                        __last_yield = 1;
                        __result = (__sunfish__::movecache->__getfast__((j+__sunfish__::E)))->__getfast__((j+__sunfish__::W));
                        return __result;
                        __after_yield_1:;
                    }
                    if (((i==__sunfish__::H1) and __eq((self->board)->__getfast__((j+__sunfish__::W)), const_4) and self->wc->__getsecond__())) {
                        __last_yield = 2;
                        __result = (__sunfish__::movecache->__getfast__((j+__sunfish__::W)))->__getfast__((j+__sunfish__::E));
                        return __result;
                        __after_yield_2:;
                    }
                END_FOR

            END_FOR

        END_FOR

        __stop_iteration = true;
        return __zero<tuple<__ss_int> *>();
    }

};

__iter<tuple<__ss_int> *> *Position::gen_moves() {
    return new __gen_Position_gen_moves(this);

}

Position *Position::rotate() {
    /**
    Rotates the board, preserving enpassant 
    */
    
    return (new Position(((this->board)->__slice__(__ss_int(4), __ss_int(0), __ss_int(0), (-__ss_int(1))))->swapcase(), (-this->score), this->bc, this->wc, ((this->ep)?((__ss_int(119)-this->ep)):(__ss_int(0))), ((this->kp)?((__ss_int(119)-this->kp)):(__ss_int(0)))));
}

Position *Position::nullmove() {
    /**
    Like rotate, but clears ep and kp 
    */
    
    return (new Position(((this->board)->__slice__(__ss_int(4), __ss_int(0), __ss_int(0), (-__ss_int(1))))->swapcase(), (-this->score), this->bc, this->wc, __ss_int(0), __ss_int(0)));
}

Position *Position::move(tuple<__ss_int> *move) {
    __ss_int ep, i, j, kp, score;
    str *__57, *__58, *board, *p, *q;
    lambda1 put;
    tuple<__ss_bool> *__59, *__60, *bc, *wc;
    tuple<__ss_int> *__56;

    __56 = move;
    __unpack_check(__56, 2);
    i = __56->__getfirst__();
    j = __56->__getsecond__();
    __57 = (this->board)->__getfast__(i);
    __58 = (this->board)->__getfast__(j);
    p = __57;
    q = __58;
    put = __lambda1__;
    board = this->board;
    __59 = this->wc;
    __60 = this->bc;
    wc = __59;
    bc = __60;
    ep = __ss_int(0);
    kp = __ss_int(0);
    score = (this->score+this->value(move));
    board = put(board, j, board->__getfast__(i));
    board = put(board, i, const_2);
    if ((i==__sunfish__::A1)) {
        wc = (new tuple<__ss_bool>(2,False,wc->__getsecond__()));
    }
    if ((i==__sunfish__::H1)) {
        wc = (new tuple<__ss_bool>(2,wc->__getfirst__(),False));
    }
    if ((j==__sunfish__::A8)) {
        bc = (new tuple<__ss_bool>(2,bc->__getfirst__(),False));
    }
    if ((j==__sunfish__::H8)) {
        bc = (new tuple<__ss_bool>(2,False,bc->__getsecond__()));
    }
    if (__eq(p, const_4)) {
        wc = (new tuple<__ss_bool>(2,False,False));
        if ((__abs((j-i))==__ss_int(2))) {
            kp = __floordiv((i+j),__ss_int(2));
            board = put(board, (((j<i))?(__sunfish__::A1):(__sunfish__::H1)), const_2);
            board = put(board, kp, const_5);
        }
    }
    if (__eq(p, const_1)) {
        if ((__sunfish__::A8<=j)&&(j<=__sunfish__::H8)) {
            board = put(board, j, const_6);
        }
        if (((j-i)==(__ss_int(2)*__sunfish__::N))) {
            ep = (i+__sunfish__::N);
        }
        if ((j==this->ep)) {
            board = put(board, (j+__sunfish__::S), const_2);
        }
    }
    return ((new Position(board, score, wc, bc, ep, kp)))->rotate();
}

__ss_int Position::value(tuple<__ss_int> *move) {
    __ss_int i, j, score;
    str *__62, *__63, *p, *q;
    tuple<__ss_int> *__61, *pstp;
    __ss_bool __64, __65;

    __61 = move;
    __unpack_check(__61, 2);
    i = __61->__getfirst__();
    j = __61->__getsecond__();
    __62 = (this->board)->__getfast__(i);
    __63 = (this->board)->__getfast__(j);
    p = __62;
    q = __63;
    pstp = __sunfish__::pst->__getitem__(p);
    score = (pstp->__getfast__(j)-pstp->__getfast__(i));
    if (q->islower()) {
        score = (score+(__sunfish__::pst->__getitem__(q->upper()))->__getfast__((__ss_int(119)-j)));
    }
    if ((__abs((j-this->kp))<__ss_int(2))) {
        score = (score+(__sunfish__::pst->__getitem__(const_4))->__getfast__((__ss_int(119)-j)));
    }
    if ((__eq(p, const_4) and (__abs((i-j))==__ss_int(2)))) {
        score = (score+(__sunfish__::pst->__getitem__(const_5))->__getfast__(__floordiv((i+j),__ss_int(2))));
        score = (score-(__sunfish__::pst->__getitem__(const_5))->__getfast__((((j<i))?(__sunfish__::A1):(__sunfish__::H1))));
    }
    if (__eq(p, const_1)) {
        if ((__sunfish__::A8<=j)&&(j<=__sunfish__::H8)) {
            score = (score+((__sunfish__::pst->__getitem__(const_6))->__getfast__(j)-(__sunfish__::pst->__getitem__(const_1))->__getfast__(j)));
        }
        if ((j==this->ep)) {
            score = (score+(__sunfish__::pst->__getitem__(const_1))->__getfast__((__ss_int(119)-(j+__sunfish__::S))));
        }
    }
    return score;
}

void Position::__static__() {
}

/**
class Entry
*/

class_ *cl_Entry;

void *Entry::__init__(__ss_int lower, __ss_int upper) {
    
    this->lower = lower;
    this->upper = upper;
    return NULL;
}

/**
class Searcher
*/

class_ *cl_Searcher;

void *Searcher::__init__() {
    
    this->tp_score = (new dict<tuple2<Position *, tuple2<__ss_int, __ss_bool> *> *, Entry *>());
    this->tp_move = (new dict<Position *, tuple<__ss_int> *>());
    this->history = (new set<Position *>());
    this->nodes = __ss_int(0);
    return NULL;
}

class __gen_Searcher_moves : public __iter<tuple2<tuple<__ss_int> *, __ss_int> *> {
public:
    void *c;
    tuple<__ss_int> *killer, *move;
    list<tuple2<__ss_int, tuple<__ss_int> *> *> *__84, *val_move;
    __ss_int __86, depth, gamma, val;
    Searcher *self;
    __ss_bool __66, __67, __72, __74, __75, __88, __89, root;
    Position *pos;
    pyobj *__73, *__76;
    tuple2<__ss_int, tuple<__ss_int> *> *__83;
    __iter<tuple2<__ss_int, tuple<__ss_int> *> *> *__85;
    list<tuple2<__ss_int, tuple<__ss_int> *> *>::for_in_loop __87;

    int __last_yield;

    __gen_Searcher_moves(Searcher *self,__ss_int depth,__ss_bool root,Position *pos,__ss_int gamma) {
        this->self = self;
        this->depth = depth;
        this->root = root;
        this->pos = pos;
        this->gamma = gamma;
        __last_yield = -1;
    }

    tuple2<tuple<__ss_int> *, __ss_int> * __get_next() {
        switch(__last_yield) {
            case 0: goto __after_yield_0;
            case 1: goto __after_yield_1;
            case 2: goto __after_yield_2;
            case 3: goto __after_yield_3;
            default: break;
        }
        if (((depth>__ss_int(0)) and __NOT(root) and any(new list_comp_4(pos)))) {
            __last_yield = 0;
            __result = (new tuple2<tuple<__ss_int> *, __ss_int>(2,NULL,(-self->bound(pos->nullmove(), (__ss_int(1)-gamma), (depth-__ss_int(3)), False))));
            return __result;
            __after_yield_0:;
        }
        if ((depth==__ss_int(0))) {
            __last_yield = 1;
            __result = (new tuple2<tuple<__ss_int> *, __ss_int>(2,NULL,pos->score));
            return __result;
            __after_yield_1:;
        }
        killer = (self->tp_move)->get(pos);
        if ((___bool(killer) and ((depth>__ss_int(0)) or (pos->value(killer)>=__sunfish__::QS_LIMIT)))) {
            __last_yield = 2;
            __result = (new tuple2<tuple<__ss_int> *, __ss_int>(2,killer,(-self->bound(pos->move(killer), (__ss_int(1)-gamma), (depth-__ss_int(1)), False))));
            return __result;
            __after_yield_2:;
        }
        val_move = list_comp_5(pos);

        FOR_IN(__83,sorted(val_move, __ss_int(0), __ss_int(0), True),84,86,87)
            __83 = __83;
            __unpack_check(__83, 2);
            val = __83->__getfirst__();
            move = __83->__getsecond__();
            if (((depth>__ss_int(0)) or (pos->value(move)>=__sunfish__::QS_LIMIT))) {
                __last_yield = 3;
                __result = (new tuple2<tuple<__ss_int> *, __ss_int>(2,move,(-self->bound(pos->move(move), (__ss_int(1)-gamma), (depth-__ss_int(1)), False))));
                return __result;
                __after_yield_3:;
            }
        END_FOR

        __stop_iteration = true;
        return __zero<tuple2<tuple<__ss_int> *, __ss_int> *>();
    }

};

__iter<tuple2<tuple<__ss_int> *, __ss_int> *> *Searcher::moves(__ss_int depth, __ss_bool root, Position *pos, __ss_int gamma) {
    return new __gen_Searcher_moves(this,depth,root,pos,gamma);

}

__ss_int Searcher::bound(Position *pos, __ss_int gamma, __ss_int depth, __ss_bool root) {
    /**
    returns r where
    s(pos) <= r < gamma    if gamma > s(pos)
    gamma <= r <= s(pos)   if gamma <= s(pos)
    */
    Entry *entry;
    __ss_int __99, best, score;
    tuple<__ss_int> *move;
    lambda2 is_dead;
    void *__101, *m;
    __ss_bool __104, __105, __106, __90, __91, __92, __93, __94, __95, in_check;
    tuple2<tuple<__ss_int> *, __ss_int> *__96;
    __iter<tuple2<tuple<__ss_int> *, __ss_int> *> *__97, *__98;
    __iter<tuple2<tuple<__ss_int> *, __ss_int> *>::for_in_loop __100;
    Searcher *__102;
    dict<Position *, tuple<__ss_int> *> *__103;
    dict<tuple2<Position *, tuple2<__ss_int, __ss_bool> *> *, Entry *> *__119, *__120;

    this->nodes = (this->nodes+__ss_int(1));
    depth = ___max(2, __ss_int(0), depth, __ss_int(0));
    if ((pos->score<=(-__sunfish__::MATE_LOWER))) {
        return (-__sunfish__::MATE_UPPER);
    }
    if (__sunfish__::DRAW_TEST) {
        if ((__NOT(root) and (this->history)->__contains__(pos))) {
            return __ss_int(0);
        }
    }
    entry = (this->tp_score)->get((new tuple2<Position *, tuple2<__ss_int, __ss_bool> *>(2,pos,(new tuple2<__ss_int, __ss_bool>(2,depth,root)))), (new Entry((-__sunfish__::MATE_UPPER), __sunfish__::MATE_UPPER)));
    if (((entry->lower>=gamma) and (__NOT(root) or ((this->tp_move)->get(pos)!=NULL)))) {
        return entry->lower;
    }
    if ((entry->upper<gamma)) {
        return entry->upper;
    }
    best = (-__sunfish__::MATE_UPPER);

    FOR_IN(__96,this->moves(depth, root, pos, gamma),97,99,100)
        __96 = __96;
        __unpack_check(__96, 2);
        move = __96->__getfirst__();
        score = __96->__getsecond__();
        best = ___max(2, __ss_int(0), best, score);
        if ((best>=gamma)) {
            if ((((__ss_float)(len(this->tp_move)))>__sunfish__::TABLE_SIZE)) {
                (this->tp_move)->clear();
            }
            this->tp_move->__setitem__(pos, move);
            break;
        }
    END_FOR

    if (((best<gamma) and (best<__ss_int(0)) and (depth>__ss_int(0)))) {
        is_dead = __lambda2__;
        if (all(new list_comp_7(is_dead, pos))) {
            in_check = is_dead(pos->nullmove());
            best = ((in_check)?((-__sunfish__::MATE_UPPER)):(__ss_int(0)));
        }
    }
    if ((((__ss_float)(len(this->tp_score)))>__sunfish__::TABLE_SIZE)) {
        (this->tp_score)->clear();
    }
    if ((best>=gamma)) {
        this->tp_score->__setitem__((new tuple2<Position *, tuple2<__ss_int, __ss_bool> *>(2,pos,(new tuple2<__ss_int, __ss_bool>(2,depth,root)))), (new Entry(best, entry->upper)));
    }
    if ((best<gamma)) {
        this->tp_score->__setitem__((new tuple2<Position *, tuple2<__ss_int, __ss_bool> *>(2,pos,(new tuple2<__ss_int, __ss_bool>(2,depth,root)))), (new Entry(entry->lower, best)));
    }
    return best;
}

class __gen_Searcher_search : public __iter<tuple2<__ss_int, tuple2<tuple<__ss_int> *, __ss_int> *> *> {
public:
    __ss_int __121, __122, __123, __124, depth, gamma, lower, score, upper;
    Searcher *self;
    Position *pos;
    list<Position *> *history;

    int __last_yield;

    __gen_Searcher_search(Searcher *self,Position *pos,list<Position *> *history) {
        this->self = self;
        this->pos = pos;
        this->history = history;
        __last_yield = -1;
    }

    tuple2<__ss_int, tuple2<tuple<__ss_int> *, __ss_int> *> * __get_next() {
        switch(__last_yield) {
            case 0: goto __after_yield_0;
            default: break;
        }
        self->nodes = __ss_int(0);
        if (__sunfish__::DRAW_TEST) {
            self->history = (new set<Position *>(history));
            (self->tp_score)->clear();
        }

        FAST_FOR(depth,__ss_int(1),__ss_int(1000),1,121,122)
            __123 = (-__sunfish__::MATE_UPPER);
            __124 = __sunfish__::MATE_UPPER;
            lower = __123;
            upper = __124;

            while ((lower<(upper-__sunfish__::EVAL_ROUGHNESS))) {
                gamma = __floordiv(((lower+upper)+__ss_int(1)),__ss_int(2));
                score = self->bound(pos, gamma, depth, True);
                if ((score>=gamma)) {
                    lower = score;
                }
                if ((score<gamma)) {
                    upper = score;
                }
            }
            self->bound(pos, lower, depth, True);
            __last_yield = 0;
            __result = (new tuple2<__ss_int, tuple2<tuple<__ss_int> *, __ss_int> *>(2,depth,(new tuple2<tuple<__ss_int> *, __ss_int>(2,(self->tp_move)->get(pos),((self->tp_score)->get((new tuple2<Position *, tuple2<__ss_int, __ss_bool> *>(2,pos,(new tuple2<__ss_int, __ss_bool>(2,depth,True))))))->lower))));
            return __result;
            __after_yield_0:;
        END_FOR

        __stop_iteration = true;
        return __zero<tuple2<__ss_int, tuple2<tuple<__ss_int> *, __ss_int> *> *>();
    }

};

__iter<tuple2<__ss_int, tuple2<tuple<__ss_int> *, __ss_int> *> *> *Searcher::search(Position *pos, list<Position *> *history) {
    /**
    Iterative deepening MTD-bi search 
    */
    return new __gen_Searcher_search(this,pos,history);

}

__ss_int parse(str *c) {
    __ss_int __125, __126, fil, rank;

    __125 = (ord(c->__getfast__(__ss_int(0)))-ord(const_7));
    __126 = (__int(c->__getfast__(__ss_int(1)))-__ss_int(1));
    fil = __125;
    rank = __126;
    return ((__sunfish__::A1+fil)-(__ss_int(10)*rank));
}

str *render(__ss_int i) {
    __ss_int fil, rank;
    tuple<__ss_int> *__127;

    __127 = divmod((i-__sunfish__::A1), __ss_int(10));
    __unpack_check(__127, 2);
    rank = __127->__getfast__(0);
    fil = __127->__getfast__(1);
    return (chr((fil+ord(const_7))))->__add__(__str(((-rank)+__ss_int(1))));
}

void *print_pos(Position *pos) {
    dict<str *, str *> *uni_pieces;
    __ss_int __131, i;
    str *row;
    void *p;
    tuple2<__ss_int, str *> *__128;
    __iter<tuple2<__ss_int, str *> *> *__129, *__130;
    list<str *> *__132;
    __iter<tuple2<__ss_int, str *> *>::for_in_loop __133;

    print(0, NULL, NULL, NULL);
    uni_pieces = (new dict<str *, str *>(13, (new tuple<str *>(2,const_5,const_8)),(new tuple<str *>(2,const_9,const_10)),(new tuple<str *>(2,const_11,const_12)),(new tuple<str *>(2,const_6,const_13)),(new tuple<str *>(2,const_4,const_14)),(new tuple<str *>(2,const_1,const_15)),(new tuple<str *>(2,const_16,const_17)),(new tuple<str *>(2,const_18,const_19)),(new tuple<str *>(2,const_20,const_21)),(new tuple<str *>(2,const_22,const_23)),(new tuple<str *>(2,const_24,const_25)),(new tuple<str *>(2,const_26,const_27)),(new tuple<str *>(2,const_2,const_28))));

    FOR_IN_ENUMERATE(row,(pos->board)->split(),132,131)
        i = __131;
        print(3, NULL, NULL, NULL, const_29, (__ss_int(8)-i), (const_29)->join(new list_comp_8(row, uni_pieces)));
    END_FOR

    print(1, NULL, NULL, NULL, const_30);
    return NULL;
}

void *__ss_main() {
    list<Position *> *hist;
    Searcher *__145, *searcher;
    tuple<__ss_int> *move;
    __re__::match_object *match;
    __ss_float start;
    __ss_int __142, _depth, score;
    tuple2<__ss_int, tuple2<tuple<__ss_int> *, __ss_int> *> *__138;
    tuple2<tuple<__ss_int> *, __ss_int> *__139;
    __iter<tuple2<__ss_int, tuple2<tuple<__ss_int> *, __ss_int> *> *> *__140, *__141;
    __iter<tuple2<__ss_int, tuple2<tuple<__ss_int> *, __ss_int> *> *>::for_in_loop __143;
    void *__144;

    hist = (new list<Position *>(1,(new Position(__sunfish__::initial, __ss_int(0), (new tuple<__ss_bool>(2,True,True)), (new tuple<__ss_bool>(2,True,True)), __ss_int(0), __ss_int(0)))));
    searcher = (new Searcher(1));

    while (True) {
        print_pos(hist->__getfast__((-__ss_int(1))));
        if (((hist->__getfast__((-__ss_int(1))))->score<=(-__sunfish__::MATE_LOWER))) {
            print(1, NULL, NULL, NULL, const_31);
            break;
        }
        move = NULL;

        while ((!((hist->__getfast__((-__ss_int(1))))->gen_moves())->__contains__(move))) {
            match = __re__::match((const_32)->__mul__(__ss_int(2)), const_33, __ss_int(0));
            if (___bool(match)) {
                move = (new tuple<__ss_int>(2,parse(match->group(1, __ss_int(1))),parse(match->group(1, __ss_int(2)))));
            }
            else {
                print(1, NULL, NULL, NULL, const_34);
            }
        }
        hist->append((hist->__getfast__((-__ss_int(1))))->move(move));
        print_pos((hist->__getfast__((-__ss_int(1))))->rotate());
        if (((hist->__getfast__((-__ss_int(1))))->score<=(-__sunfish__::MATE_LOWER))) {
            print(1, NULL, NULL, NULL, const_35);
            break;
        }
        start = __time__::time();

        FOR_IN(__138,searcher->search(hist->__getfast__((-__ss_int(1))), hist),140,142,143)
            __138 = __138;
            _depth = __138->__getfirst__();
            __139 = __138->__getsecond__();
            __unpack_check(__139, 2);
            move = __139->__getfirst__();
            score = __139->__getsecond__();
            if ((_depth==__ss_int(8))) {
                break;
            }
        END_FOR

        if ((score==__sunfish__::MATE_UPPER)) {
            print(1, NULL, NULL, NULL, const_36);
        }
        print(2, NULL, NULL, NULL, const_37, (render((__ss_int(119)-move->__getfirst__())))->__add__(render((__ss_int(119)-move->__getsecond__()))));
        hist->append((hist->__getfast__((-__ss_int(1))))->move(move));
        break;
    }
    return NULL;
}

void __init() {
    const_0 = new str("RBNQ");
    const_1 = __char_cache[80];
    const_2 = __char_cache[46];
    const_3 = new str("PNK");
    const_4 = __char_cache[75];
    const_5 = __char_cache[82];
    const_6 = __char_cache[81];
    const_7 = __char_cache[97];
    const_8 = new str("\342\231\234");
    const_9 = __char_cache[78];
    const_10 = new str("\342\231\236");
    const_11 = __char_cache[66];
    const_12 = new str("\342\231\235");
    const_13 = new str("\342\231\233");
    const_14 = new str("\342\231\232");
    const_15 = new str("\342\231\237");
    const_16 = __char_cache[114];
    const_17 = new str("\342\231\226");
    const_18 = __char_cache[110];
    const_19 = new str("\342\231\230");
    const_20 = __char_cache[98];
    const_21 = new str("\342\231\227");
    const_22 = __char_cache[113];
    const_23 = new str("\342\231\225");
    const_24 = __char_cache[107];
    const_25 = new str("\342\231\224");
    const_26 = __char_cache[112];
    const_27 = new str("\342\231\231");
    const_28 = new str("\302\267");
    const_29 = __char_cache[32];
    const_30 = new str("    a b c d e f g h \n\n");
    const_31 = new str("You lost");
    const_32 = new str("([a-h][1-8])");
    const_33 = new str("d2d4");
    const_34 = new str("Please enter a move like g8f6");
    const_35 = new str("You won");
    const_36 = new str("Checkmate!");
    const_37 = new str("My move:");
    const_38 = new str("         \n         \n rnbqkbnr\n pppppppp\n ........\n ........\n ........\n ........\n PPPPPPPP\n RNBQKBNR\n         \n         \n");
    const_39 = new str("__main__");

    __name__ = new str("__main__");

    movecount = __ss_int(0);
    piece = (new dict<str *, __ss_int>(6, (new tuple2<str *, __ss_int >(2,const_1,__ss_int(100))),(new tuple2<str *, __ss_int >(2,const_9,__ss_int(280))),(new tuple2<str *, __ss_int >(2,const_11,__ss_int(320))),(new tuple2<str *, __ss_int >(2,const_5,__ss_int(479))),(new tuple2<str *, __ss_int >(2,const_6,__ss_int(929))),(new tuple2<str *, __ss_int >(2,const_4,__ss_int(60000)))));
    pst = (new dict<str *, tuple<__ss_int> *>(6, (new tuple2<str *, tuple<__ss_int> *>(2,const_1,(new tuple<__ss_int>(64,__ss_int(0),__ss_int(0),__ss_int(0),__ss_int(0),__ss_int(0),__ss_int(0),__ss_int(0),__ss_int(0),__ss_int(78),__ss_int(83),__ss_int(86),__ss_int(73),__ss_int(102),__ss_int(82),__ss_int(85),__ss_int(90),__ss_int(7),__ss_int(29),__ss_int(21),__ss_int(44),__ss_int(40),__ss_int(31),__ss_int(44),__ss_int(7),(-__ss_int(17)),__ss_int(16),(-__ss_int(2)),__ss_int(15),__ss_int(14),__ss_int(0),__ss_int(15),(-__ss_int(13)),(-__ss_int(26)),__ss_int(3),__ss_int(10),__ss_int(9),__ss_int(6),__ss_int(1),__ss_int(0),(-__ss_int(23)),(-__ss_int(22)),__ss_int(9),__ss_int(5),(-__ss_int(11)),(-__ss_int(10)),(-__ss_int(2)),__ss_int(3),(-__ss_int(19)),(-__ss_int(31)),__ss_int(8),(-__ss_int(7)),(-__ss_int(37)),(-__ss_int(36)),(-__ss_int(14)),__ss_int(3),(-__ss_int(31)),__ss_int(0),__ss_int(0),__ss_int(0),__ss_int(0),__ss_int(0),__ss_int(0),__ss_int(0),__ss_int(0))))),(new tuple2<str *, tuple<__ss_int> *>(2,const_9,(new tuple<__ss_int>(64,(-__ss_int(66)),(-__ss_int(53)),(-__ss_int(75)),(-__ss_int(75)),(-__ss_int(10)),(-__ss_int(55)),(-__ss_int(58)),(-__ss_int(70)),(-__ss_int(3)),(-__ss_int(6)),__ss_int(100),(-__ss_int(36)),__ss_int(4),__ss_int(62),(-__ss_int(4)),(-__ss_int(14)),__ss_int(10),__ss_int(67),__ss_int(1),__ss_int(74),__ss_int(73),__ss_int(27),__ss_int(62),(-__ss_int(2)),__ss_int(24),__ss_int(24),__ss_int(45),__ss_int(37),__ss_int(33),__ss_int(41),__ss_int(25),__ss_int(17),(-__ss_int(1)),__ss_int(5),__ss_int(31),__ss_int(21),__ss_int(22),__ss_int(35),__ss_int(2),__ss_int(0),(-__ss_int(18)),__ss_int(10),__ss_int(13),__ss_int(22),__ss_int(18),__ss_int(15),__ss_int(11),(-__ss_int(14)),(-__ss_int(23)),(-__ss_int(15)),__ss_int(2),__ss_int(0),__ss_int(2),__ss_int(0),(-__ss_int(23)),(-__ss_int(20)),(-__ss_int(74)),(-__ss_int(23)),(-__ss_int(26)),(-__ss_int(24)),(-__ss_int(19)),(-__ss_int(35)),(-__ss_int(22)),(-__ss_int(69)))))),(new tuple2<str *, tuple<__ss_int> *>(2,const_11,(new tuple<__ss_int>(64,(-__ss_int(59)),(-__ss_int(78)),(-__ss_int(82)),(-__ss_int(76)),(-__ss_int(23)),(-__ss_int(107)),(-__ss_int(37)),(-__ss_int(50)),(-__ss_int(11)),__ss_int(20),__ss_int(35),(-__ss_int(42)),(-__ss_int(39)),__ss_int(31),__ss_int(2),(-__ss_int(22)),(-__ss_int(9)),__ss_int(39),(-__ss_int(32)),__ss_int(41),__ss_int(52),(-__ss_int(10)),__ss_int(28),(-__ss_int(14)),__ss_int(25),__ss_int(17),__ss_int(20),__ss_int(34),__ss_int(26),__ss_int(25),__ss_int(15),__ss_int(10),__ss_int(13),__ss_int(10),__ss_int(17),__ss_int(23),__ss_int(17),__ss_int(16),__ss_int(0),__ss_int(7),__ss_int(14),__ss_int(25),__ss_int(24),__ss_int(15),__ss_int(8),__ss_int(25),__ss_int(20),__ss_int(15),__ss_int(19),__ss_int(20),__ss_int(11),__ss_int(6),__ss_int(7),__ss_int(6),__ss_int(20),__ss_int(16),(-__ss_int(7)),__ss_int(2),(-__ss_int(15)),(-__ss_int(12)),(-__ss_int(14)),(-__ss_int(15)),(-__ss_int(10)),(-__ss_int(10)))))),(new tuple2<str *, tuple<__ss_int> *>(2,const_5,(new tuple<__ss_int>(64,__ss_int(35),__ss_int(29),__ss_int(33),__ss_int(4),__ss_int(37),__ss_int(33),__ss_int(56),__ss_int(50),__ss_int(55),__ss_int(29),__ss_int(56),__ss_int(67),__ss_int(55),__ss_int(62),__ss_int(34),__ss_int(60),__ss_int(19),__ss_int(35),__ss_int(28),__ss_int(33),__ss_int(45),__ss_int(27),__ss_int(25),__ss_int(15),__ss_int(0),__ss_int(5),__ss_int(16),__ss_int(13),__ss_int(18),(-__ss_int(4)),(-__ss_int(9)),(-__ss_int(6)),(-__ss_int(28)),(-__ss_int(35)),(-__ss_int(16)),(-__ss_int(21)),(-__ss_int(13)),(-__ss_int(29)),(-__ss_int(46)),(-__ss_int(30)),(-__ss_int(42)),(-__ss_int(28)),(-__ss_int(42)),(-__ss_int(25)),(-__ss_int(25)),(-__ss_int(35)),(-__ss_int(26)),(-__ss_int(46)),(-__ss_int(53)),(-__ss_int(38)),(-__ss_int(31)),(-__ss_int(26)),(-__ss_int(29)),(-__ss_int(43)),(-__ss_int(44)),(-__ss_int(53)),(-__ss_int(30)),(-__ss_int(24)),(-__ss_int(18)),__ss_int(5),(-__ss_int(2)),(-__ss_int(18)),(-__ss_int(31)),(-__ss_int(32)))))),(new tuple2<str *, tuple<__ss_int> *>(2,const_6,(new tuple<__ss_int>(64,__ss_int(6),__ss_int(1),(-__ss_int(8)),(-__ss_int(104)),__ss_int(69),__ss_int(24),__ss_int(88),__ss_int(26),__ss_int(14),__ss_int(32),__ss_int(60),(-__ss_int(10)),__ss_int(20),__ss_int(76),__ss_int(57),__ss_int(24),(-__ss_int(2)),__ss_int(43),__ss_int(32),__ss_int(60),__ss_int(72),__ss_int(63),__ss_int(43),__ss_int(2),__ss_int(1),(-__ss_int(16)),__ss_int(22),__ss_int(17),__ss_int(25),__ss_int(20),(-__ss_int(13)),(-__ss_int(6)),(-__ss_int(14)),(-__ss_int(15)),(-__ss_int(2)),(-__ss_int(5)),(-__ss_int(1)),(-__ss_int(10)),(-__ss_int(20)),(-__ss_int(22)),(-__ss_int(30)),(-__ss_int(6)),(-__ss_int(13)),(-__ss_int(11)),(-__ss_int(16)),(-__ss_int(11)),(-__ss_int(16)),(-__ss_int(27)),(-__ss_int(36)),(-__ss_int(18)),__ss_int(0),(-__ss_int(19)),(-__ss_int(15)),(-__ss_int(15)),(-__ss_int(21)),(-__ss_int(38)),(-__ss_int(39)),(-__ss_int(30)),(-__ss_int(31)),(-__ss_int(13)),(-__ss_int(31)),(-__ss_int(36)),(-__ss_int(34)),(-__ss_int(42)))))),(new tuple2<str *, tuple<__ss_int> *>(2,const_4,(new tuple<__ss_int>(64,__ss_int(4),__ss_int(54),__ss_int(47),(-__ss_int(99)),(-__ss_int(99)),__ss_int(60),__ss_int(83),(-__ss_int(62)),(-__ss_int(32)),__ss_int(10),__ss_int(55),__ss_int(56),__ss_int(56),__ss_int(55),__ss_int(10),__ss_int(3),(-__ss_int(62)),__ss_int(12),(-__ss_int(57)),__ss_int(44),(-__ss_int(67)),__ss_int(28),__ss_int(37),(-__ss_int(31)),(-__ss_int(55)),__ss_int(50),__ss_int(11),(-__ss_int(4)),(-__ss_int(19)),__ss_int(13),__ss_int(0),(-__ss_int(49)),(-__ss_int(55)),(-__ss_int(43)),(-__ss_int(52)),(-__ss_int(28)),(-__ss_int(51)),(-__ss_int(47)),(-__ss_int(8)),(-__ss_int(50)),(-__ss_int(47)),(-__ss_int(42)),(-__ss_int(43)),(-__ss_int(79)),(-__ss_int(64)),(-__ss_int(32)),(-__ss_int(29)),(-__ss_int(32)),(-__ss_int(4)),__ss_int(3),(-__ss_int(14)),(-__ss_int(50)),(-__ss_int(57)),(-__ss_int(18)),__ss_int(13),__ss_int(4),__ss_int(17),__ss_int(30),(-__ss_int(3)),(-__ss_int(14)),__ss_int(6),(-__ss_int(1)),__ss_int(40),__ss_int(18)))))));

    FOR_IN(__0,(new list<tuple2<str *, tuple<__ss_int> *> *>(__sunfish__::pst->items())),1,3,4)
        __0 = __0;
        __unpack_check(__0, 2);
        k = __0->__getfirst__();
        table = __0->__getsecond__();
        padrow = __lambda0__;
        __sunfish__::pst->__setitem__(__sunfish__::k, __sum(new list_comp_1(), (new tuple<void *>())));
        __sunfish__::pst->__setitem__(__sunfish__::k, ((((new tuple<__ss_int>(1,__ss_int(0))))->__mul__(__ss_int(20)))->__add__(__sunfish__::pst->__getitem__(__sunfish__::k)))->__add__(((new tuple<__ss_int>(1,__ss_int(0))))->__mul__(__ss_int(20))));
    END_FOR

    movecache = list_comp_3();
    A1 = __ss_int(91);
    H1 = __ss_int(98);
    A8 = __ss_int(21);
    H8 = __ss_int(28);
    initial = const_38;
    __15 = (-__ss_int(10));
    __16 = (-__ss_int(1));
    N = __15;
    E = __ss_int(1);
    S = __ss_int(10);
    W = __16;
    directions = (new dict<str *, tuple<__ss_int> *>(6, (new tuple2<str *, tuple<__ss_int> *>(2,const_1,(new tuple<__ss_int>(4,__sunfish__::N,(__sunfish__::N+__sunfish__::N),(__sunfish__::N+__sunfish__::W),(__sunfish__::N+__sunfish__::E))))),(new tuple2<str *, tuple<__ss_int> *>(2,const_9,(new tuple<__ss_int>(8,((__sunfish__::N+__sunfish__::N)+__sunfish__::E),((__sunfish__::E+__sunfish__::N)+__sunfish__::E),((__sunfish__::E+__sunfish__::S)+__sunfish__::E),((__sunfish__::S+__sunfish__::S)+__sunfish__::E),((__sunfish__::S+__sunfish__::S)+__sunfish__::W),((__sunfish__::W+__sunfish__::S)+__sunfish__::W),((__sunfish__::W+__sunfish__::N)+__sunfish__::W),((__sunfish__::N+__sunfish__::N)+__sunfish__::W))))),(new tuple2<str *, tuple<__ss_int> *>(2,const_11,(new tuple<__ss_int>(4,(__sunfish__::N+__sunfish__::E),(__sunfish__::S+__sunfish__::E),(__sunfish__::S+__sunfish__::W),(__sunfish__::N+__sunfish__::W))))),(new tuple2<str *, tuple<__ss_int> *>(2,const_5,(new tuple<__ss_int>(4,__sunfish__::N,__sunfish__::E,__sunfish__::S,__sunfish__::W)))),(new tuple2<str *, tuple<__ss_int> *>(2,const_6,(new tuple<__ss_int>(8,__sunfish__::N,__sunfish__::E,__sunfish__::S,__sunfish__::W,(__sunfish__::N+__sunfish__::E),(__sunfish__::S+__sunfish__::E),(__sunfish__::S+__sunfish__::W),(__sunfish__::N+__sunfish__::W))))),(new tuple2<str *, tuple<__ss_int> *>(2,const_4,(new tuple<__ss_int>(8,__sunfish__::N,__sunfish__::E,__sunfish__::S,__sunfish__::W,(__sunfish__::N+__sunfish__::E),(__sunfish__::S+__sunfish__::E),(__sunfish__::S+__sunfish__::W),(__sunfish__::N+__sunfish__::W)))))));
    MATE_LOWER = (__sunfish__::piece->__getitem__(const_4)-(__ss_int(10)*__sunfish__::piece->__getitem__(const_6)));
    MATE_UPPER = (__sunfish__::piece->__getitem__(const_4)+(__ss_int(10)*__sunfish__::piece->__getitem__(const_6)));
    TABLE_SIZE = __ss_float(10000000.0);
    QS_LIMIT = __ss_int(219);
    EVAL_ROUGHNESS = __ss_int(13);
    DRAW_TEST = True;
    cl_Position = new class_("Position");
    Position::__static__();
    cl_Entry = new class_("Entry");
    default_0 = True;
    default_1 = (new list<Position *>());
    cl_Searcher = new class_("Searcher");
    if (__eq(__sunfish__::__name__, const_39)) {
        __ss_main();
    }
}

} // module namespace

int main(int, char **) {
    __shedskin__::__init();
    __re__::__init();
    __time__::__init();
    __itertools__::__init();
    __shedskin__::__start(__sunfish__::__init);
}
