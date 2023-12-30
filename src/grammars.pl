% This is grammar file for prolog , here we write Predicates and atoms for predicates .Facts and relation  to compare them , and get

% You can place your Predicate and atoms , then make relation . 
% "%" sign represents  single line comment . 

% Here , Likes is predicate and shyam and ram are atoms
likes(shyam,ram).

% Below are shyam, atom with 3 additional queries each 
likes(shyam,ram,hari,sahar).
likes(shyam,alam,asham,asrif).

likes(dhanbrd,pau).
likes(man,suarha).
dislikes(ram,shyam).
dislikes(tato,matu).
dislikes(shyam,sahar,pawan).
love(muna,madhan).
love(matu,tato).
love(mohan,madhu).
love (madhu,mohan).
love (sita,ram).
unique(asrif,asham,alam,satori,sham,shamim,shamima).
love(ram,sita).


% -------------------_ CONDITIONS _-----------------------------------------
% The friend is a  Predicate defining relation with conditions of Previous Predicates 

% So, this should return true , likes (shyam,ram ) and not(dislikes(ram,shyam))
friend(X,Y) :- likes(X,Y); notdislikes(X,Y) .
enemy(X,Y) :- dislikes(X,Y), love(Y,X); not dislike(X,X), likes(Y,Y).

% Those two Z coz error , bocz jealous only takes two arguments those are X and Y
jealous( X , Y ) :- love(X,Y), love(Y,Y), not love(X,Y).




%  This is relation with queries , add many as you want .
% Remember  " ," is equivalent to and ,
%           ";" is equivalent to or 
%           "not"  is equivalent to not i.e negation
%           ":-" is equivalent to if then 
%
%  Remember Error with small level is Warned with Red coloured . and Those grammar blocks are ignored..

