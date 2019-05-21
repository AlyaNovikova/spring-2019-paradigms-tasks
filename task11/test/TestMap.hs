{-# LANGUAGE ScopedTypeVariables #-}  -- Включаем некоторые расширения компилятора.
import Test.Tasty
import Test.Tasty.HUnit
import Data.Proxy
import Map
import qualified Data.Map.Strict as SMap
import MapInstance
import NaiveList(NaiveList)  -- Импортируем только тип NaiveList, но не его конструкторы Nil/Cons, чтобы не путались с конструкторами NaiveTree.
import NaiveTree

main :: IO ()
main = defaultMain testMap

{-|
  Генерирует группу тестов для конкретной реализации 'Map'
  с определённым именем.

  Мы хотим писать тесты один раз для всех возможных реализаций 'Map'.
  В чистом Haskell нам может помочь параметрический полиморфизм,
  но для этого нужно, чтобы в сигнатуре функции присутствовал
  тип из класса 'Map', который мы хотим протестировать.

  Специально для этих целей существует обёртка 'Data.Proxy', он
  позволяет передавать в функции даже типы высшего порядка.
-}
mapTests :: Map m => String -> Proxy m -> TestTree
mapTests name (_ :: Proxy m) =
    -- Чтобы можно было связать типовую переменную m здесь и в let ниже, нужно расширение ScopedTypeVariables.
    testGroup name [
        testGroup "Smoke tests" [
            testCase "toAscList . fromList sorts list" $
                let tr = fromList [(2, "a"), (1, "b"), (3, "c"), (1, "x")] :: m Int String in
                toAscList tr @?= [(1, "x"), (2, "a"), (3, "c")]
        ],

        testGroup "insert" [
            testCase "insert in empty map" $
                let map = insert 1 "a" (empty :: m Int String) in
                Map.lookup 1 map @?= Just "a",
            testCase "insert existing key" $
                let map = insert 1 "a" (fromList [(1, "b"), (2, "b")]) :: m Int String in
                Map.lookup 1 map @?= Just "a",
            testCase "insert new key" $
                let map = insert 1 "a" (fromList [(2, "b"), (3, "c")]) :: m Int String in
                Map.lookup 1 map @?= Just "a"
        ],

        testGroup "insertWith" [
            testCase "insertWith in empty map" $
                let map = insertWith (++) 1 "a" (empty :: m Int String) in
                Map.lookup 1 map @?= Just "a",
            testCase "insertWith existing key" $
                let map = insertWith (++) 1 "a" (fromList [(1, "b"), (2, "b")]) :: m Int String in
                Map.lookup 1 map @?= Just "ab",
            testCase "insertWith new key" $
                let map = insert 1 "a" (fromList [(2, "b"), (3, "c")]) :: m Int String in
                Map.lookup 1 map @?= Just "a"
        ],

        let f key new_value old_value = show key ++ new_value ++ old_value in
        testGroup "insertWithKey" [
            testCase "insertWithKey in empty map" $
                let map = insertWithKey f 1 "a" (empty :: m Int String) in
                Map.lookup 1 map @?= Just "a",
            testCase "insertWithKey existing key" $
                let map = insertWithKey f 1 "a" (fromList [(1, "b"), (2, "b")]) :: m Int String in
                Map.lookup 1 map @?= Just "1ab",
            testCase "insertWithKey new key" $
                let map = insertWithKey f 1 "a" (fromList [(2, "b"), (3, "c")]) :: m Int String in
                Map.lookup 1 map @?= Just "a"
        ],

        testGroup "delete" [
            testCase "delete empty map" $
                let map = delete 1 empty :: m Int String in do
                Map.notMember 1 map @?= True
                Map.size map @?= 0,
            testCase "delete existing key" $
                let map = delete 1 (fromList [(1, "b"), (2, "b")]) :: m Int String in do
                Map.notMember 1 map @?= True
                Map.size map @?= 1,
            testCase "delete non-existent key" $
                let map = delete 1 (fromList [(2, "b"), (3, "c")]) :: m Int String in do
                Map.notMember 1 map @?= True
                Map.size map @?= 2
        ],

        testGroup "adjust" [
            testCase "adjust on empty map" $
                let map = adjust ("new" ++) 1 (empty :: m Int String) in
                Map.null map @?= True,
            testCase "adjust existing key" $
                let map = adjust ("new " ++) 1 (fromList [(1, "a"), (2, "b")] :: m Int String) in
                Map.lookup 1 map @?= Just "new a",
            testCase "adjust non-existent key" $
                let map = adjust ("new" ++ ) 1 (fromList [(2, "a"), (3, "b")] :: m Int String) in
                Map.lookup 1 map @?= Nothing
        ],

        let f key x = show key ++ x in
        testGroup "adjustWithKey" [
            testCase "adjustWithKey on empty map" $
                let map = adjustWithKey f 1 (empty :: m Int String) in
                Map.null map @?= True,
            testCase "adjustWithKey existing key" $
                let map = adjustWithKey f 1 (fromList [(1, "a"), (2, "b")] :: m Int String) in
                Map.lookup 1 map @?= Just "1a",
            testCase "adjustWithKey non-existent key" $
                let map = adjustWithKey f 1 (fromList [(2, "a"), (3, "b")] :: m Int String) in
                Map.lookup 1 map @?= Nothing
        ],

        let f x = if x == "a" then Just "new a" else Nothing in
        testGroup "update" [
            testCase "update existing key" $
                let map = update f 1 (fromList [(1, "a"), (2, "a")]) :: m Int String in do
                Map.lookup 1 map @?= Just "new a"
                Map.lookup 2 map @?= Just "a",
            testCase "update non-existent key" $
                let map = update f 1 (fromList [(2, "a"), (3, "b")]) :: m Int String in
                Map.lookup 1 map @?= Nothing
        ],

        let f k x = if x == "a" then Just (show k ++ " new a") else Nothing in
        testGroup "updateWithKey" [
            testCase "updateWithKey existing key" $
                let map = updateWithKey f 1 (fromList [(1, "a"), (2, "a")]) :: m Int String in do
                Map.lookup 1 map @?= Just "1 new a"
                Map.lookup 2 map @?= Just "a",
            testCase "updateWithKey non-existent key" $
                let map = updateWithKey f 1 (fromList [(2, "a"), (3, "b")]) :: m Int String in
                Map.lookup 1 map @?= Nothing
        ],

        testGroup "member" [
            testCase "member in empty map" $
                let map = empty :: m Int String in
                Map.member 1 map @?= False,
            testCase "member - existing key" $
                let map = fromList [(1, "a"), (2, "b")] :: m Int String in
                Map.member 1 map @?= True,
            testCase "member - non-existent key" $
                let map = fromList [(1, "a"), (2, "b")] :: m Int String in
                Map.member 3 map @?= False
        ],

        testGroup "notMember" [
            testCase "notMember in empty map" $
                let map = empty :: m Int String in
                Map.notMember 1 map @?= True,
            testCase "notMember - existing key" $
                let map = fromList [(1, "a"), (2, "b")] :: m Int String in
                Map.notMember 1 map @?= False,
            testCase "notMember - non-existent key" $
                let map = fromList [(1, "a"), (2, "b")] :: m Int String in
                Map.notMember 3 map @?= True
        ],

        testGroup "null" [
            testCase "null on empty map" $
                let map = empty :: m Int String in
                Map.null map @?= True,
            testCase "null on non-empty map" $
                let map = fromList [(1, "a"), (2, "b")] :: m Int String in
                Map.null map @?= False
        ]
    ]

testNaiveTree :: TestTree
testNaiveTree = testGroup "Test NaiveTree" [
        testGroup "merge" [
            testCase "merge empty" $
                merge Nil Nil @?= (Nil :: NaiveTree () ())
            ,
            testCase "merge two nodes" $
                -- Ваша реализация может выдавать другое дерево, соответствующее
                -- последовательности 1, 2.
                merge (Node 1 "a" Nil Nil) (Node 2 "b" Nil Nil)
                    @?= Node 1 "a" Nil (Node 2 "b" Nil Nil)
        ]
    ]

testMap :: TestTree
testMap = testGroup "Testing implementations of trees"
    [
        mapTests "Data.Map.Strict" (Proxy :: Proxy SMap.Map),
        mapTests "NaiveList" (Proxy :: Proxy NaiveList),
        mapTests "NaiveTree" (Proxy :: Proxy NaiveTree),
        testNaiveTree
    ]
