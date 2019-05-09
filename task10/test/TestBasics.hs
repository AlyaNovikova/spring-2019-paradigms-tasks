import Test.Tasty
import Test.Tasty.HUnit

import Basics

main :: IO ()
main = defaultMain testsBasics

testsBasics :: TestTree
testsBasics = testGroup "Unit tests for Basics tasks"
    [testCase "head' works on non-empty list" $
        head' [1,2,3] @?= 1

    , testCase "head' works on infinite list" $
        head' [1..] @?= 1

    , testCase "tail' works on non-empty list too" $
        tail' [1,2,3] @?= [2,3]

    , testCase "tail' works on infinite list" $
        take' 100 (tail' [1..]) @?= take' 100 [2..]

    , testCase "take' takes 1 element from 3-element list" $
        take' 1 [1,2,3] @?= [1]

    , testCase "take' takes 2 element from 2-element list" $
        take' 2 ["a", "b"] @?= ["a", "b"]

    , testCase "take' takes 2 element from infinite list" $
        take' 2 [1..] @?= [1, 2]

    , testCase "drop' drops 1 element from 3-element list" $
        drop' 1 [1,2,3] @?= [2,3]

    , testCase "drop' drops 2 element from 2-element list" $
        drop' 2 [10, 2] @?= []

    , testCase "drop' drops 1 elements from infinite list" $
        take' 100 (drop' 1 [1..]) @?= take' 100 [2..]

    , testCase "filter' selects only even numbers from 0 to 10" $
        filter' even [0..10] @?= [0,2..10]

    , testCase "filter' works on infinite list" $
        take' 100 (filter' even [1..]) @?= take' 100 [2, 4..]

    , testCase "foldl'' can be used for finding sum of elements" $
        foldl'' (+) 0 [1,2,3] @?= 6

    , testCase "foldl'' works on empty list" $
        foldl'' (+) (-1) [] @?= -1

    , testCase "foldl'' works for non-associative operation" $
        foldl'' (-) (-2) [4, 2, 0] @?= (-8)

    , testCase "concat' works on finite lists as expected" $
        concat' [1,2,3] [4,5,6] @?= [1..6]

    , testCase "concat' works on infinite first list" $
        take' 100 (concat' [1..] [239, 239]) @?= take' 100 [1..]

    , testCase "concat' works on infinite second list" $
        take' 100 (concat' [1] [2..]) @?= take' 100 [1..]

    , testCase "quickSort actualy sorts the list" $
        quickSort' [5,2,3,4,1] @?= [1..5]

    , testCase "quickSort actualy sorts the small list" $
        quickSort' [1] @?= [1]
    ]
