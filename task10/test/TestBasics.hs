import Test.Tasty
import Test.Tasty.HUnit

import Basics

main :: IO ()
main = defaultMain testsBasics

testsBasics :: TestTree
testsBasics = testGroup "Unit tests for Basics tasks"
    [testCase "head' works on non-empty list" $
        head' [1,2,3] @?= 1

    , testCase "head' works on non-empty list2" $
        head' [("a", "b"),("c", "b"),("d", "e")] @?= ("a", "b")

    , testCase "head' works on infinite list" $
        head' [1..] @?= 1

    , testCase "tail' works on non-empty list too" $
        tail' [1,2,3] @?= [2,3]

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

    , testCase "filter' selects only even numbers from 0 to 10" $
        filter' even [0..10] @?= [0,2..10]

    , testCase "filter' selects only odd numbers from 0 to 10" $
        filter' odd [0..10] @?= [1,3..9]

    , testCase "foldl'' can be used for finding sum of elements" $
        foldl'' (+) 0 [1,2,3] @?= 6

    , testCase "foldl'' can be used for finding sum of elements" $
        foldl'' (+) (-1) [] @?= -1

    , testCase "foldl'' can be used for finding sum of elements" $
        foldl'' (+) (-1) [1] @?= 0

    , testCase "concat' works on finite lists as expected" $
        concat' [1,2,3] [4,5,6] @?= [1..6]

    , testCase "quickSort actualy sorts the list" $
        quickSort' [5,2,3,4,1] @?= [1..5]

    , testCase "quickSort actualy sorts the list" $
        quickSort' [1] @?= [1]
    ]
