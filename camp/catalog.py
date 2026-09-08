"""OpenCamp catalog — only free, public CP resources."""

from __future__ import annotations

# Every link is a public page: no paid course, no login wall required to read.

MODULES = [
    {
        "id": "bootcamp",
        "order": 1,
        "band": "Gray → 800",
        "title": "Bootcamp",
        "blurb": "I/O, complexity, and the first 20 Codeforces problems. Finish this before you touch graphs.",
        "hours": "1–2 weeks",
        "theory": [
            {"title": "Competitive Programmer's Handbook, Ch. 1–2 (free PDF)", "url": "https://cses.fi/book/book.pdf", "source": "CSES"},
            {"title": "USACO Guide — Introducing Competitive Programming", "url": "https://usaco.guide/general/intro-cp", "source": "USACO Guide"},
            {"title": "GeeksforGeeks — DSA hub (free articles)", "url": "https://www.geeksforgeeks.org/dsa/dsa-tutorial-learn-data-structures-and-algorithms/", "source": "GeeksforGeeks"},
            {"title": "Errichto — C++ for competitive programming", "url": "https://www.youtube.com/watch?v=LamhEkxmP1Q", "source": "YouTube"},
        ],
        "problems": [
            {"id": "cf-4a", "name": "Watermelon", "oj": "Codeforces", "rating": 800, "url": "https://codeforces.com/problemset/problem/4/A", "note": "First accepted. If/else + parity."},
            {"id": "cf-71a", "name": "Way Too Long Words", "oj": "Codeforces", "rating": 800, "url": "https://codeforces.com/problemset/problem/71/A", "note": "String I/O."},
            {"id": "cf-231a", "name": "Team", "oj": "Codeforces", "rating": 800, "url": "https://codeforces.com/problemset/problem/231/A"},
            {"id": "cf-158a", "name": "Next Round", "oj": "Codeforces", "rating": 800, "url": "https://codeforces.com/problemset/problem/158/A"},
            {"id": "cf-50a", "name": "Domino piling", "oj": "Codeforces", "rating": 800, "url": "https://codeforces.com/problemset/problem/50/A"},
            {"id": "cf-282a", "name": "Bit++", "oj": "Codeforces", "rating": 800, "url": "https://codeforces.com/problemset/problem/282/A"},
            {"id": "cf-263a", "name": "Beautiful Matrix", "oj": "Codeforces", "rating": 800, "url": "https://codeforces.com/problemset/problem/263/A"},
            {"id": "cf-112a", "name": "Petya and Strings", "oj": "Codeforces", "rating": 800, "url": "https://codeforces.com/problemset/problem/112/A"},
            {"id": "cf-339a", "name": "Helpful Maths", "oj": "Codeforces", "rating": 800, "url": "https://codeforces.com/problemset/problem/339/A"},
            {"id": "cses-1068", "name": "Weird Algorithm", "oj": "CSES", "rating": 800, "url": "https://cses.fi/problemset/task/1068", "note": "Collatz. Learn the CSES judge."},
            {"id": "cses-1083", "name": "Missing Number", "oj": "CSES", "rating": 800, "url": "https://cses.fi/problemset/task/1083"},
            {"id": "abc-abs", "name": "AtCoder Beginners Selection", "oj": "AtCoder", "rating": 800, "url": "https://atcoder.jp/contests/abs", "note": "Practice set, not one task. Do Practice A–D."},
        ],
    },
    {
        "id": "impl",
        "order": 2,
        "band": "800–1000",
        "title": "Implementation",
        "blurb": "Turn a worded rule into loops. Most Div. 2 A/B problems live here.",
        "hours": "1 week",
        "theory": [
            {"title": "USACO Guide — Ad Hoc Problems", "url": "https://usaco.guide/bronze/ad-hoc", "source": "USACO Guide"},
            {"title": "CSES introductory problems", "url": "https://cses.fi/problemset/", "source": "CSES"},
            {"title": "GeeksforGeeks — Hashing", "url": "https://www.geeksforgeeks.org/dsa/hashing-data-structure/", "source": "GeeksforGeeks"},
            {"title": "GeeksforGeeks — Stack", "url": "https://www.geeksforgeeks.org/dsa/stack-data-structure/", "source": "GeeksforGeeks"},
        ],
        "problems": [
            {"id": "cses-1069", "name": "Repetitions", "oj": "CSES", "rating": 800, "url": "https://cses.fi/problemset/task/1069"},
            {"id": "cses-1094", "name": "Increasing Array", "oj": "CSES", "rating": 800, "url": "https://cses.fi/problemset/task/1094"},
            {"id": "cses-1070", "name": "Permutations", "oj": "CSES", "rating": 900, "url": "https://cses.fi/problemset/task/1070"},
            {"id": "cses-1071", "name": "Number Spiral", "oj": "CSES", "rating": 1000, "url": "https://cses.fi/problemset/task/1071"},
            {"id": "cf-677a", "name": "Vanya and Fence", "oj": "Codeforces", "rating": 800, "url": "https://codeforces.com/problemset/problem/677/A"},
            {"id": "cf-734a", "name": "Anton and Danik", "oj": "Codeforces", "rating": 800, "url": "https://codeforces.com/problemset/problem/734/A"},
            {"id": "cf-791a", "name": "Bear and Big Brother", "oj": "Codeforces", "rating": 800, "url": "https://codeforces.com/problemset/problem/791/A"},
            {"id": "cf-977a", "name": "Wrong Subtraction", "oj": "Codeforces", "rating": 800, "url": "https://codeforces.com/problemset/problem/977/A"},
            {"id": "cf-1328a", "name": "Divisibility Problem", "oj": "Codeforces", "rating": 800, "url": "https://codeforces.com/problemset/problem/1328/A"},
            {"id": "cf-1335a", "name": "Candies and Two Sisters", "oj": "Codeforces", "rating": 800, "url": "https://codeforces.com/problemset/problem/1335/A"},
        ],
    },
    {
        "id": "math",
        "order": 3,
        "band": "800–1200",
        "title": "Math & number theory",
        "blurb": "Mods, gcd, primes, combinatorics. Read the article, then grind the CSES math section.",
        "hours": "1–2 weeks",
        "theory": [
            {"title": "CP-Algorithms — Binary exponentiation", "url": "https://cp-algorithms.com/algebra/binary-exp.html", "source": "CP-Algorithms"},
            {"title": "CP-Algorithms — Sieve of Eratosthenes", "url": "https://cp-algorithms.com/algebra/sieve-of-eratosthenes.html", "source": "CP-Algorithms"},
            {"title": "CP-Algorithms — Euclidean algorithm", "url": "https://cp-algorithms.com/algebra/euclid-algorithm.html", "source": "CP-Algorithms"},
            {"title": "USACO Guide — Modular arithmetic", "url": "https://usaco.guide/gold/modular", "source": "USACO Guide"},
            {"title": "Handbook Ch. 21 — Number theory (PDF)", "url": "https://cses.fi/book/book.pdf", "source": "CSES"},
        ],
        "problems": [
            {"id": "cses-1617", "name": "Bit Strings", "oj": "CSES", "rating": 900, "url": "https://cses.fi/problemset/task/1617"},
            {"id": "cses-1618", "name": "Trailing Zeros", "oj": "CSES", "rating": 1000, "url": "https://cses.fi/problemset/task/1618"},
            {"id": "cses-1754", "name": "Coin Piles", "oj": "CSES", "rating": 1000, "url": "https://cses.fi/problemset/task/1754"},
            {"id": "cf-230b", "name": "T-primes", "oj": "Codeforces", "rating": 1300, "url": "https://codeforces.com/problemset/problem/230/B", "note": "Sieve + perfect squares."},
            {"id": "cf-26a", "name": "Almost Prime", "oj": "Codeforces", "rating": 900, "url": "https://codeforces.com/problemset/problem/26/A"},
            {"id": "cf-472a", "name": "Design Tutorial: Learn from Math", "oj": "Codeforces", "rating": 800, "url": "https://codeforces.com/problemset/problem/472/A"},
            {"id": "cf-1352c", "name": "K-th Not Divisible by n", "oj": "Codeforces", "rating": 1200, "url": "https://codeforces.com/problemset/problem/1352/C"},
        ],
    },
    {
        "id": "greedy",
        "order": 4,
        "band": "900–1400",
        "title": "Sorting, greedy, scanning",
        "blurb": "Sort, then prove a choice is safe. CSES Sorting and Searching is the cleanest free set on the internet.",
        "hours": "2 weeks",
        "theory": [
            {"title": "USACO Guide — Introduction to Greedy", "url": "https://usaco.guide/bronze/intro-greedy", "source": "USACO Guide"},
            {"title": "USACO Guide — Greedy with sorting (Silver)", "url": "https://usaco.guide/silver/greedy-sorting", "source": "USACO Guide"},
            {"title": "CP-Algorithms — Scheduling problems", "url": "https://cp-algorithms.com/schedules/schedule-description.html", "source": "CP-Algorithms"},
            {"title": "Errichto — Greedy algorithms", "url": "https://www.youtube.com/watch?v=H-QsB2MgcxM", "source": "YouTube"},
            {"title": "GeeksforGeeks — Kadane / activity selection", "url": "https://www.geeksforgeeks.org/dsa/largest-sum-contiguous-subarray/", "source": "GeeksforGeeks"},
        ],
        "problems": [
            {"id": "cses-1621", "name": "Distinct Numbers", "oj": "CSES", "rating": 800, "url": "https://cses.fi/problemset/task/1621"},
            {"id": "cses-1084", "name": "Apartments", "oj": "CSES", "rating": 1000, "url": "https://cses.fi/problemset/task/1084"},
            {"id": "cses-1090", "name": "Ferris Wheel", "oj": "CSES", "rating": 1100, "url": "https://cses.fi/problemset/task/1090"},
            {"id": "cses-1629", "name": "Movie Festival", "oj": "CSES", "rating": 1200, "url": "https://cses.fi/problemset/task/1629"},
            {"id": "cses-1640", "name": "Sum of Two Values", "oj": "CSES", "rating": 1100, "url": "https://cses.fi/problemset/task/1640"},
            {"id": "cses-1643", "name": "Maximum Subarray Sum", "oj": "CSES", "rating": 1200, "url": "https://cses.fi/problemset/task/1643", "note": "Kadane."},
            {"id": "cses-1074", "name": "Stick Lengths", "oj": "CSES", "rating": 1200, "url": "https://cses.fi/problemset/task/1074"},
            {"id": "cf-337a", "name": "Puzzles", "oj": "Codeforces", "rating": 900, "url": "https://codeforces.com/problemset/problem/337/A"},
            {"id": "cf-489b", "name": "BerSU Ball", "oj": "Codeforces", "rating": 1200, "url": "https://codeforces.com/problemset/problem/489/B"},
            {"id": "cf-580a", "name": "Kefa and First Steps", "oj": "Codeforces", "rating": 900, "url": "https://codeforces.com/problemset/problem/580/A"},
        ],
    },
    {
        "id": "search",
        "order": 5,
        "band": "1100–1600",
        "title": "Binary search & two pointers",
        "blurb": "When the answer is monotonic, search on it. Codeforces EDU is free and better than most paid courses.",
        "hours": "1–2 weeks",
        "theory": [
            {"title": "Codeforces EDU — Binary Search (free course)", "url": "https://codeforces.com/edu/course/2/lesson/6", "source": "CF EDU"},
            {"title": "CP-Algorithms — Binary search", "url": "https://cp-algorithms.com/num_methods/binary_search.html", "source": "CP-Algorithms"},
            {"title": "USACO Guide — Binary search on the answer", "url": "https://usaco.guide/silver/binary-search", "source": "USACO Guide"},
            {"title": "USACO Guide — Two pointers", "url": "https://usaco.guide/silver/two-pointers", "source": "USACO Guide"},
        ],
        "problems": [
            {"id": "cses-1620", "name": "Factory Machines", "oj": "CSES", "rating": 1400, "url": "https://cses.fi/problemset/task/1620"},
            {"id": "cses-1085", "name": "Array Division", "oj": "CSES", "rating": 1500, "url": "https://cses.fi/problemset/task/1085"},
            {"id": "cf-706b", "name": "Interesting drink", "oj": "Codeforces", "rating": 1100, "url": "https://codeforces.com/problemset/problem/706/B"},
            {"id": "cf-474b", "name": "Worms", "oj": "Codeforces", "rating": 1200, "url": "https://codeforces.com/problemset/problem/474/B"},
            {"id": "cf-279b", "name": "Books", "oj": "Codeforces", "rating": 1400, "url": "https://codeforces.com/problemset/problem/279/B"},
            {"id": "cf-492b", "name": "Vanya and Lanterns", "oj": "Codeforces", "rating": 1200, "url": "https://codeforces.com/problemset/problem/492/B"},
            {"id": "cses-1641", "name": "Sum of Three Values", "oj": "CSES", "rating": 1500, "url": "https://cses.fi/problemset/task/1641"},
        ],
    },
    {
        "id": "prefix",
        "order": 6,
        "band": "1000–1500",
        "title": "Prefix sums & difference arrays",
        "blurb": "O(1) range queries after O(n) prep. Silver staple.",
        "hours": "4–6 days",
        "theory": [
            {"title": "USACO Guide — Prefix sums", "url": "https://usaco.guide/silver/prefix-sums", "source": "USACO Guide"},
            {"title": "USACO Guide — More prefix sums", "url": "https://usaco.guide/silver/more-prefix-sums", "source": "USACO Guide"},
            {"title": "CP-Algorithms — Range queries (static)", "url": "https://cp-algorithms.com/data_structures/sparse-table.html", "source": "CP-Algorithms"},
        ],
        "problems": [
            {"id": "cses-1646", "name": "Static Range Sum Queries", "oj": "CSES", "rating": 900, "url": "https://cses.fi/problemset/task/1646"},
            {"id": "cses-1660", "name": "Subarray Sums I", "oj": "CSES", "rating": 1300, "url": "https://cses.fi/problemset/task/1660"},
            {"id": "cses-1661", "name": "Subarray Sums II", "oj": "CSES", "rating": 1500, "url": "https://cses.fi/problemset/task/1661"},
            {"id": "cf-433b", "name": "Kuriyama Mirai's Stones", "oj": "Codeforces", "rating": 1200, "url": "https://codeforces.com/problemset/problem/433/B"},
            {"id": "cf-816b", "name": "Karen and Coffee", "oj": "Codeforces", "rating": 1400, "url": "https://codeforces.com/problemset/problem/816/B"},
            {"id": "usaco-hps", "name": "Why Did the Cow Cross the Road II", "oj": "USACO", "rating": 1300, "url": "http://www.usaco.org/index.php?page=viewproblem2&cpid=715"},
        ],
    },
    {
        "id": "graphs1",
        "order": 7,
        "band": "1200–1700",
        "title": "Graphs I — BFS & DFS",
        "blurb": "Represent the graph, then walk it. CSES Graph Algorithms is the standard free syllabus.",
        "hours": "2 weeks",
        "theory": [
            {"title": "CP-Algorithms — Breadth-first search", "url": "https://cp-algorithms.com/graph/breadth-first-search.html", "source": "CP-Algorithms"},
            {"title": "CP-Algorithms — Depth-first search", "url": "https://cp-algorithms.com/graph/depth-first-search.html", "source": "CP-Algorithms"},
            {"title": "USACO Guide — Graph traversal", "url": "https://usaco.guide/silver/graph-traversal", "source": "USACO Guide"},
            {"title": "USACO Guide — Flood fill", "url": "https://usaco.guide/silver/ff", "source": "USACO Guide"},
            {"title": "Errichto — DFS / BFS", "url": "https://www.youtube.com/watch?v=Q9wXuojp2v8", "source": "YouTube"},
        ],
        "problems": [
            {"id": "cses-1666", "name": "Building Roads", "oj": "CSES", "rating": 1200, "url": "https://cses.fi/problemset/task/1666"},
            {"id": "cses-1668", "name": "Building Teams", "oj": "CSES", "rating": 1300, "url": "https://cses.fi/problemset/task/1668", "note": "Bipartite check."},
            {"id": "cses-1667", "name": "Message Route", "oj": "CSES", "rating": 1300, "url": "https://cses.fi/problemset/task/1667"},
            {"id": "cses-1669", "name": "Round Trip", "oj": "CSES", "rating": 1400, "url": "https://cses.fi/problemset/task/1669"},
            {"id": "cf-500a", "name": "New Year Transportation", "oj": "Codeforces", "rating": 1000, "url": "https://codeforces.com/problemset/problem/500/A"},
            {"id": "cf-520b", "name": "Two Buttons", "oj": "Codeforces", "rating": 1400, "url": "https://codeforces.com/problemset/problem/520/B"},
            {"id": "cf-580c", "name": "Kefa and Park", "oj": "Codeforces", "rating": 1500, "url": "https://codeforces.com/problemset/problem/580/C"},
        ],
    },
    {
        "id": "graphs2",
        "order": 8,
        "band": "1500–1900",
        "title": "Graphs II — shortest paths & DSU",
        "blurb": "Dijkstra, Floyd, union-find. Watch CF EDU DSU, then CSES shortest routes.",
        "hours": "2 weeks",
        "theory": [
            {"title": "CP-Algorithms — Dijkstra", "url": "https://cp-algorithms.com/graph/dijkstra.html", "source": "CP-Algorithms"},
            {"title": "CP-Algorithms — Bellman–Ford", "url": "https://cp-algorithms.com/graph/bellman_ford.html", "source": "CP-Algorithms"},
            {"title": "CP-Algorithms — DSU", "url": "https://cp-algorithms.com/data_structures/disjoint_set_union.html", "source": "CP-Algorithms"},
            {"title": "Codeforces EDU — DSU", "url": "https://codeforces.com/edu/course/2/lesson/7", "source": "CF EDU"},
            {"title": "USACO Guide — Shortest paths", "url": "https://usaco.guide/gold/shortest-paths", "source": "USACO Guide"},
        ],
        "problems": [
            {"id": "cses-1671", "name": "Shortest Routes I", "oj": "CSES", "rating": 1500, "url": "https://cses.fi/problemset/task/1671"},
            {"id": "cses-1672", "name": "Shortest Routes II", "oj": "CSES", "rating": 1500, "url": "https://cses.fi/problemset/task/1672"},
            {"id": "cses-1195", "name": "Flight Discount", "oj": "CSES", "rating": 1700, "url": "https://cses.fi/problemset/task/1195"},
            {"id": "cses-1675", "name": "Road Reparation", "oj": "CSES", "rating": 1400, "url": "https://cses.fi/problemset/task/1675", "note": "MST."},
            {"id": "cses-1676", "name": "Road Construction", "oj": "CSES", "rating": 1400, "url": "https://cses.fi/problemset/task/1676"},
            {"id": "cf-20c", "name": "Dijkstra?", "oj": "Codeforces", "rating": 1900, "url": "https://codeforces.com/problemset/problem/20/C"},
            {"id": "cf-893c", "name": "Loyalty", "oj": "Codeforces", "rating": 1400, "url": "https://codeforces.com/problemset/problem/893/C"},
        ],
    },
    {
        "id": "dp",
        "order": 9,
        "band": "1400–1900",
        "title": "Dynamic programming",
        "blurb": "State, transition, order. CSES DP is the free gold set; AtCoder DP contest is the other.",
        "hours": "3 weeks",
        "theory": [
            {"title": "CP-Algorithms — Introduction to DP", "url": "https://cp-algorithms.com/dynamic_programming/intro-to-dp.html", "source": "CP-Algorithms"},
            {"title": "CP-Algorithms — Knapsack", "url": "https://cp-algorithms.com/dynamic_programming/knapsack.html", "source": "CP-Algorithms"},
            {"title": "USACO Guide — Intro to DP", "url": "https://usaco.guide/gold/intro-dp", "source": "USACO Guide"},
            {"title": "AtCoder DP contest editorial hub", "url": "https://atcoder.jp/contests/dp/tasks", "source": "AtCoder"},
            {"title": "Errichto — DP", "url": "https://www.youtube.com/watch?v=YBSt2jYkXIs", "source": "YouTube"},
        ],
        "problems": [
            {"id": "cses-1633", "name": "Dice Combinations", "oj": "CSES", "rating": 1200, "url": "https://cses.fi/problemset/task/1633"},
            {"id": "cses-1634", "name": "Minimizing Coins", "oj": "CSES", "rating": 1400, "url": "https://cses.fi/problemset/task/1634"},
            {"id": "cses-1635", "name": "Coin Combinations I", "oj": "CSES", "rating": 1500, "url": "https://cses.fi/problemset/task/1635"},
            {"id": "cses-1638", "name": "Grid Paths", "oj": "CSES", "rating": 1500, "url": "https://cses.fi/problemset/task/1638"},
            {"id": "cses-1158", "name": "Book Shop", "oj": "CSES", "rating": 1600, "url": "https://cses.fi/problemset/task/1158"},
            {"id": "cses-1639", "name": "Edit Distance", "oj": "CSES", "rating": 1600, "url": "https://cses.fi/problemset/task/1639"},
            {"id": "atc-dp-a", "name": "Frog 1", "oj": "AtCoder", "rating": 1200, "url": "https://atcoder.jp/contests/dp/tasks/dp_a"},
            {"id": "atc-dp-d", "name": "Knapsack 1", "oj": "AtCoder", "rating": 1400, "url": "https://atcoder.jp/contests/dp/tasks/dp_d"},
            {"id": "cf-189a", "name": "Cut Ribbon", "oj": "Codeforces", "rating": 1300, "url": "https://codeforces.com/problemset/problem/189/A"},
            {"id": "cf-455a", "name": "Boredom", "oj": "Codeforces", "rating": 1500, "url": "https://codeforces.com/problemset/problem/455/A"},
        ],
    },
    {
        "id": "trees-str",
        "order": 10,
        "band": "1500–2000",
        "title": "Trees, strings, range queries",
        "blurb": "After DP, this is the usual Gold/Div. 2 D toolkit. Segment tree from CP-Algorithms, not a paid sheet.",
        "hours": "3 weeks",
        "theory": [
            {"title": "USACO Guide — Tree diameters", "url": "https://usaco.guide/gold/all-roots", "source": "USACO Guide"},
            {"title": "CP-Algorithms — String hashing", "url": "https://cp-algorithms.com/string/string-hashing.html", "source": "CP-Algorithms"},
            {"title": "CP-Algorithms — Prefix function (KMP)", "url": "https://cp-algorithms.com/string/prefix-function.html", "source": "CP-Algorithms"},
            {"title": "CP-Algorithms — Segment tree", "url": "https://cp-algorithms.com/data_structures/segment_tree.html", "source": "CP-Algorithms"},
            {"title": "Codeforces EDU — Segment tree, part 1", "url": "https://codeforces.com/edu/course/2/lesson/4", "source": "CF EDU"},
        ],
        "problems": [
            {"id": "cses-1674", "name": "Subordinates", "oj": "CSES", "rating": 1200, "url": "https://cses.fi/problemset/task/1674"},
            {"id": "cses-1131", "name": "Tree Diameter", "oj": "CSES", "rating": 1400, "url": "https://cses.fi/problemset/task/1131"},
            {"id": "cses-1734", "name": "Distinct Values Queries", "oj": "CSES", "rating": 1800, "url": "https://cses.fi/problemset/task/1734"},
            {"id": "cses-1648", "name": "Dynamic Range Sum Queries", "oj": "CSES", "rating": 1500, "url": "https://cses.fi/problemset/task/1648"},
            {"id": "cses-1753", "name": "String Matching", "oj": "CSES", "rating": 1400, "url": "https://cses.fi/problemset/task/1753"},
            {"id": "cf-339d", "name": "Xenia and Bit Operations", "oj": "Codeforces", "rating": 1700, "url": "https://codeforces.com/problemset/problem/339/D"},
        ],
    },
]

SHELVES = [
    {
        "title": "Canonical free syllabus",
        "links": [
            {"name": "USACO Guide", "url": "https://usaco.guide/", "why": "Bronze → Plat roadmap, articles + problem lists."},
            {"name": "CSES Problem Set", "url": "https://cses.fi/problemset/", "why": "300 well-ordered tasks. The standard grind."},
            {"name": "Competitive Programmer's Handbook", "url": "https://cses.fi/book/book.pdf", "why": "Free PDF that matches CSES."},
            {"name": "GeeksforGeeks DSA", "url": "https://www.geeksforgeeks.org/dsa/dsa-tutorial-learn-data-structures-and-algorithms/", "why": "Short articles on hashing, graphs, DP. Use after a miss, not as the whole syllabus."},
        ],
    },
    {
        "title": "Judges & contests (free accounts)",
        "links": [
            {"name": "Codeforces", "url": "https://codeforces.com/", "why": "Best regular contests + editorials. Use the API in Contests."},
            {"name": "AtCoder", "url": "https://atcoder.jp/", "why": "ABC every week. Cleaner statements than CF for beginners."},
            {"name": "Codeforces EDU", "url": "https://codeforces.com/edu/course/2", "why": "ITMO course: binary search, DSU, segment tree — free."},
            {"name": "USACO", "url": "http://www.usaco.org/", "why": "Official monthly contests. Archive is public."},
        ],
    },
    {
        "title": "Free video",
        "links": [
            {"name": "Errichto", "url": "https://www.youtube.com/@Errichto", "why": "Algorithms + live CF. Start with C++ for CP."},
            {"name": "SecondThread", "url": "https://www.youtube.com/@SecondThread", "why": "USACO / Codeforces streams."},
            {"name": "Colin Galen", "url": "https://www.youtube.com/@ColinGalen", "why": "Topic streams and virtuals."},
            {"name": "William Lin", "url": "https://www.youtube.com/@tmwilliamlin168", "why": "Contest VODs; watch how a red coder starts a problem."},
        ],
    },
]


def all_problems() -> list[dict]:
    out = []
    for m in MODULES:
        for p in m["problems"]:
            out.append({**p, "module_id": m["id"], "module": m["title"]})
    return out


def module_by_id(mid: str) -> dict:
    return next(m for m in MODULES if m["id"] == mid)


def problem_by_id(pid: str) -> dict:
    return next(p for p in all_problems() if p["id"] == pid)
