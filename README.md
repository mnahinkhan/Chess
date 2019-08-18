For the YouTube introduction, see: https://youtu.be/S1pXtoCKW-U


Chess program with AI

Ensure that Pygame is installed

GUI inspired by:
https://en.lichess.org/

Chess board image was taken from lichess website as well.
The images for the pieces came from:
https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Chess_Pieces_Sprite.svg/2000px-Chess_Pieces_Sprite.svg.png

AI ideas from:
https://chessprogramming.wikispaces.com/

An online lecture that helped me understand alpha-beta pruning:
Winston, P. [MIT OpenCourseWare]. (2010) 6. Search: Games, Minimax,
and Alpha-Beta. [Video File]. Retrieved from https://www.youtube.com/watch?v=STjW3eH0Cik

Special thanks to professor Saquib for being so amazing.

This program is a chess game. The user may play against a friend or the
computer.

The game state is mainly stored as a 2D list of strings, and most of the
processing is thus done on a list of strings.

The GUI takes the current state and displays it on the screen. The GUI allows
drag and drop movement of pieces as well as click-click movement.

The AI that plays against the human evaluates all possible moves made by either
player up to a certain level of depth. The AI evaluates each position by giving
it a score. The higher the value of the score, the more favourable a position
is for white and the lower the value of the score, the more favourable the
position is for black. Knowing that white will try to get the score to be higher
and black will try and get the score to be lower, the AI assumes best play from
either side as it traverses up the search tree and chooses the best move to be
played. A problem that may arise is the number of postions that need to be
evaulated. Even at 3 levels of depth, thousands of positions have to be
evaluatd.
Several methods are used in this program to reduce positions that are searched:
1. Alpha-beta pruning: As a result of  evaluating a position it can be found
that a portion of the search tree can be ignored as no further evaluations can
guarantee better results. This can happen because white and black area against
one another. White plays what is best for it and black plays what is best for it,
so it would make sense for white to ignore any portion of the tree where black
has a clear upperhand that it can choose to play.
2. Transposition table: Often, two different pathways in a search tree can result
in the same board being evaluated. Instead of evaluating the same board several
times, the program stores a table of values in a dictionary where the keys are
the positions. This way, repeated positions can have their evaluations looked up
fairly quickly, as the board state is hashed.
3. Opening Book - The opening book is again a dictionary that stores board
positions often seen in the beginning few moves in chess. Appropraite moves that
can be played at such positions is stored in the dictionary. A random move is
selected and played from the list of suggested moves wihtout searching if the AI
finds itself confronting a such a board postion. Note that this opening book was
recorded by myself and so it does not have many positions stored in it.

In order to traverse the search tree as above, the AI needs to know how to evaluate the
board at any position to decide if white or black has the advantage. My evaluation
function currently looks at three main things when evaluating the board:
   a) Material for white and black. Each piece has a value and the more pieces you have,
       the better off your position is likely to be. For example, if white has an extra
       queen, it has an advantage over black.
   b) Piece-square table values - for each piece, there is a table that stores the best
       squares that the particular piece should occupy. So if white has a knight at a
       good square that controls the centre of the board, whereas black has a knight
       at the corner of the board, the situation is evaluated as being more favourable
       for white.
   c) Reduction in points for doubled pawns, isolated pawns, and blocked pawns. If any
       side has a set of pawns with the above features their points are slightly lower
       to indicate a slight disadvantage in such a position.
   d) A checkmate: a position where this has occured gets a very high point, so that the
       AI moves towards this if it can. (or avoids it).

There are also several ways in which this program may be improved:
1. Move ordering: Given a certain position and the AI needs to search a few layers
deep from it, somehow pre-sorting each move by ranking them in their likelihood of
being good moves allows for earlier cut-offs to be made by alpha-beta pruning.
2. Iterative Deepening: Instead of going directly to a given depth when searching,
the A.I. may evaluate the best move at depth 1, then depth 2, then depth 3, etc.
until it reaches the final depth it needed to calculate at depth n. The reason for
this is that it may be mathematically shown that this does not dignificantly increase
computation and allows the A.I. to make its best move if it needs to abide by a
time limit.
3. Better data structure - I believe the structure I have used to keep the state of
the board (list of a list) may be slowing down accessing its elements or assigning
its elements. Improvement in efficiency of my code by changing data structures may
potentially improve the speed at which my AI makes its move.
4. Import of large opening tables: There are databases available online that store
the best moves played by grandmasters at various key opening positions of the chess
game. Although my AI does make use of an opening table that I recorded for it myself,
it is not able to respond to many opening positions using the table since the table
only convers few positions. If an opening table with millions of positions could be
imported to this program, the AI's moves would improve in the beginning. It would also
give it more variety in terms of the move it plays. Furthermore, using good openings
allows the AI to make the best moves in the field it is best at: middle game tactics.
5. Better evaluation of positions - The current features evaluated by the evaluation
function when judging a positoin to give it a score allows for good opening games and
tactics that often allow it to gain advantage over the opponents that I have tested it
against. However, there are many aspects of playing good chess that it does not
consider: like having good mobility of your pieces (eg a trapped bishop should be bad
for the AI but it doesn't know that). Other aspects include king safety, pawn structure,
etc. It could also use different evaluation for each game phase. For example, a pawn is
not worth much at the opening phase of the game but in the endgame it is very important
and so should be evaulated as a valuable piece.
6. Endgame tables - As good as my AI may be in middle games, given a queen and a king to
attempt checkmate against a lone king, it would be unlikely for it to succeed. This is
because such checkmates, despite being simple, require a large number of combination of
moves to occur, the depth of which my AI would not be able to see. So endgame table allows
it to know (for a very large number of endgame positions) the best move to play in order
to attempt a win or a draw (or try its best to avoid a loss).


Note about coordinates:
Normally, algebraic notation is used to specify a box on a chess board. In this
program, coordinates will be index referecnes to the 2_D array that stores the
state of the board. Thus, e4 in algebraic notation would be expressed as (4,4)
in this program.
