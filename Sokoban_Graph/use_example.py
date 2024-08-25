from retriever import graph_retriever
import sys
import asyncio

query = """"
Domain:
(define (domain sokoban)
	(:requirements :strips)
	(:predicates (sokoban ?x)   								;sokoban is at location x
				 (crate ?x)     								;crate is at location x
				 (leftOf ?x ?y) 								;location x is to the left of locaiton y
				 (below ?x ?y)  								;location x is below location y
				 (at ?x ?y)     								;object x is at location y
				 (clear ?x))									;x is a location

	(:action moveLeft
		:parameters (?sokoban ?x ?y)
		:precondition (and (sokoban ?sokoban)
						   (at ?sokoban ?x)
						   (leftOf ?y ?x)   					;location y is to the left of location x
						   (clear ?y))      					;and y is empty/clear, so move left to y
		:effect (and (at ?sokoban ?y) (clear ?x)
				(not (at ?sokoban ?x)) (not (clear ?y))))

	(:action moveRight
		:parameters (?sokoban ?x ?y)
		:precondition (and (sokoban ?sokoban)
							(at ?sokoban ?x)
							(leftOf ?x ?y)    					;location x is to the left of y
							(clear ?y))       					;and y is clear, so move right to y
		:effect (and (at ?sokoban ?y) (clear ?x)
				(not (at ?sokoban ?x)) (not (clear ?y))))

	(:action moveUp
		:parameters (?sokoban ?x ?y)
		:precondition (and (sokoban ?sokoban)
						  (at ?sokoban ?x)
						  (below ?x ?y)      					;location x is below location y
						  (clear ?y))        					;and y is clear, so move up to y
		:effect (and (at ?sokoban ?y) (clear ?x)
				(not (at ?sokoban ?x)) (not (clear ?y))))

	(:action moveDown
		:parameters (?sokoban ?x ?y)
		:precondition (and (sokoban ?sokoban)
						  (at ?sokoban ?x)
						  (below ?y ?x)      					;location y is below location x
						  (clear ?y))        					;and y is clear, so move down to y
		:effect (and (at ?sokoban ?y) (clear ?x)
				(not (at ?sokoban ?x)) (not (clear ?y))))

	(:action pushLeft
		:parameters (?sokoban ?x ?y ?z ?crate)
		:precondition (and (sokoban ?sokoban)
							(crate ?crate)
							(leftOf ?y ?x)  					;location y is left of x
							(leftOf ?z ?y)    					;z (destination for block) is left of where the block currently is
							(at ?sokoban ?x)   					;sokoban player is at x
							(at ?crate ?y)     					;crate is at y							    					
							(clear ?z))        					;and location z is clear, so push crate left to z
		:effect (and (at ?sokoban ?y) (at ?crate ?z) 
				(clear ?x) 
				(not (at ?sokoban ?x)) 
				(not (at ?crate ?y)) 
				(not (clear ?z)) 
				(not (clear ?y))))
			   
	(:action pushRight
		:parameters (?sokoban ?x ?y ?z ?crate)
		:precondition (and (sokoban ?sokoban)
							(crate ?crate)
							(leftOf ?x ?y)						;x is left of y
							(leftOf ?y ?z)						;y is left of z
							(at ?sokoban ?x)					;sokoban is at x
							(at ?crate ?y)						;crate is at y
							(clear ?z))							;z is clear, so push crate right to z
		:effect (and (at ?sokoban ?y) (at ?crate ?z) 
				(clear ?x)
				(not (at ?sokoban ?x))
				(not (at ?crate ?y))
				(not (clear ?z))
				(not (clear ?y))))

	(:action pushUp
		:parameters (?sokoban ?x ?y ?z ?crate)
		:precondition (and (sokoban ?sokoban)
							(crate ?crate)
							(below ?x ?y)						;x is below y
							(below ?y ?z)						;y is below z
							(at ?sokoban ?x)					;sokoban is at x
							(at ?crate ?y)						;crate is at y
							(clear ?z))							;z is clear, so push crate up to z
		:effect (and (at ?sokoban ?y) (at ?crate ?z)
				(clear ?x)
				(not (at ?sokoban ?x))
				(not (at ?crate ?y))
				(not (clear ?y))
				(not (clear ?z))))

	(:action pushDown
		:parameters (?sokoban ?x ?y ?z ?crate)
		:precondition (and (sokoban ?sokoban)
							(crate ?crate)
							(below ?y ?x)						;y is below x
							(below ?z ?y)						;z is below y
							(at ?sokoban ?x)					;sokoban is at x
							(at ?crate ?y)						;crate is at y
							(clear ?z))							;z is clear, so push crate down to z
		:effect (and (at ?sokoban ?y) (at ?crate ?z)
				(clear ?x)
				(not (at ?sokoban ?x))
				(not (at ?crate ?y))
				(not (clear ?y))
				(not (clear ?z))))
)

Example problems:
(define (problem s1)
	(:domain sokoban)
	(:objects sokoban, crate2, l1, l2, l5, l6, l9, l10, l11, l12, l13, l14, l15, l16, l17, l18)
	(:init (sokoban sokoban) 
		   (crate crate2)

		   ;;horizontal relationships
		   (leftOf l1 l2) 
		   (leftOf l5 l6) 
		   (leftOf l9 l10) (leftOf l10 l11) (leftOf l11 l12) 
 		   (leftOf l13 l14) (leftOf l14 l15) (leftOf l15 l16)
 		   (leftOf l17 l18)

 		   ;;vertical relationships
 		   (below l5 l1) (below l6 l2)
 		   (below l9 l5) (below l10 l6)
 		   (below l13 l9) (below l14 l10) (below l15 l11) (below l16 l12)
 		   (below l17 l13) (below l18 l14)

 		   ;;initialize sokoban and crate
		   (at sokoban l10)
 		   (at crate2 l15) 

 		   ;;clear spaces
		   (clear l1) 
		   (clear l2) 
		   (clear l5) 
		   (clear l6) 
		   (clear l9)
		   (clear l11)
		   (clear l12) 
		   (clear l13) 
		   (clear l14)
		   (clear l16) 
		   (clear l17)   				
		   (clear l18))

	(:goal (and (at crate2 l2)))
)
```

```
(define (problem s2)
	(:domain sokoban)
	(:objects sokoban1, sokoban2, crate1, crate2, l1, l2, l5, l6, l9, l10, l11, l12, l13, l14, l15, l16, l17, l18)
	(:init (sokoban sokoban1) 
		   (sokoban sokoban2)
		   (crate crate1)	
		   (crate crate2)
		   
		   ;;horizontal relationships
		   (leftOf l1 l2) 
		   (leftOf l5 l6) 
		   (leftOf l9 l10) (leftOf l10 l11) (leftOf l11 l12) 
 		   (leftOf l13 l14) (leftOf l14 l15) (leftOf l15 l16)
 		   (leftOf l17 l18)

 		   ;;vertical relationships
 		   (below l5 l1) (below l6 l2)
 		   (below l9 l5) (below l10 l6)
 		   (below l13 l9) (below l14 l10) (below l15 l11) (below l16 l12)
 		   (below l17 l13) (below l18 l14)

 		   ;;initialize sokoban and crate
		   (at sokoban1 l10)
		   (at sokoban2 l16)
		   (at crate1 l9)
 		   (at crate2 l15) 

 		   ;;clear spaces
		   (clear l1) 
		   (clear l2) 
		   (clear l5) 
		   (clear l6) 
		   (clear l11)
		   (clear l12) 
		   (clear l13) 
		   (clear l14)
		   (clear l17)   				
		   (clear l18))

	(:goal (and (at crate1 l9) (at crate2 l2)))
)

There is a simple strategy for solving all problems in this domain without using search. Implement the strategy as a Python function.

The code should should be of the form

def get_plan(objects, init, goal):
# Your code here
return plan

where
- `objects` is a set of objects (string names)
- `init` is a set of ground atoms represented as tuples of predicate
names and arguments (e.g., ('predicate-foo', 'object-bar', ...))
- `goal` is also a set of ground atoms represented in the same way
- `plan` is a list of actions, where each action is a ground operator
represented as a string (e.g., '(operator-baz object-qux ...)')

You only need to generate python programs, no explanation is required!

"""



# 將標準輸出重定向到 log.txt 文件
async def main():
    sys.stdout = open('exp2.txt', 'w')
    print("prompt 加入 You only need to generate python programs, no explanation is required!")
    print("\n--------------------------------------------------")
    
    # 確保使用 await 等待協程的結果
    result = await graph_retriever(query)
    print(result)
    
    sys.stdout.close()

# 用 asyncio.run() 來運行這個異步函數
asyncio.run(main())