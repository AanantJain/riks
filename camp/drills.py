"""In-app drills: original statements, skills from free public sources.

Statements are written here (not copied from Codeforces). Sources are the
handbook / guide articles the student should read after a miss.
"""

from __future__ import annotations

from camp.learner import effective_skill, expected_score

DRILLS: list[dict] = [
    # --- Bootcamp ---
    {
        "id": "d-boot-even",
        "module_id": "bootcamp",
        "title": "Even split",
        "type": "mcq",
        "rating": 800,
        "source": {"title": "CPH Ch. 1 — Introduction", "url": "https://cses.fi/book/book.pdf"},
        "text": "A bar of chocolate weighs w grams. You may break it into two pieces whose weights are positive integers that add to w. Can both pieces have even weight when w = 8? When w = 3?",
        "options": ["8 yes, 3 yes", "8 yes, 3 no", "8 no, 3 yes", "both no"],
        "answer": "8 yes, 3 no",
        "explanation": "Need two positive even integers summing to w, so w even and w ≥ 4. 8 = 2+6; 3 is odd.",
    },
    {
        "id": "d-boot-yesno",
        "module_id": "bootcamp",
        "title": "Parity gate",
        "type": "code",
        "rating": 800,
        "source": {"title": "USACO Guide — Introducing CP", "url": "https://usaco.guide/general/intro-cp"},
        "text": "Read one integer w (1 ≤ w ≤ 100). Print YES if w is even and at least 4, otherwise NO. (This is the even-split check as a program.)",
        "sample": {"stdin": "8\n", "stdout": "YES\n"},
        "starter": "w = int(input())\n# print YES or NO\n",
        "tests": [
            {"stdin": "8\n", "stdout": "YES\n"},
            {"stdin": "3\n", "stdout": "NO\n"},
            {"stdin": "2\n", "stdout": "NO\n", "hidden": True},
            {"stdin": "100\n", "stdout": "YES\n", "hidden": True},
        ],
        "explanation": "w % 2 == 0 and w >= 4.",
    },
    {
        "id": "d-boot-complex",
        "module_id": "bootcamp",
        "title": "What is the complexity?",
        "type": "mcq",
        "rating": 800,
        "source": {"title": "CP-Algorithms — time complexity", "url": "https://cp-algorithms.com/others/time_complexity.html"},
        "text": "for i in 1..n:\n    for j in 1..i:\n        s += 1\nHow many times does s += 1 run?",
        "options": ["n", "n²", "n(n+1)/2", "2^n"],
        "answer": "n(n+1)/2",
        "explanation": "Inner loop runs 1+2+…+n = n(n+1)/2. That is Θ(n²).",
    },
    {
        "id": "d-boot-collatz",
        "module_id": "bootcamp",
        "title": "Weird sequence",
        "type": "short",
        "rating": 800,
        "source": {"title": "CSES Weird Algorithm (skill)", "url": "https://cses.fi/problemset/task/1068"},
        "text": "Start at n = 6. Repeatedly: if n is even, n ← n/2; else n ← 3n+1. Write the sequence until 1, space-separated.",
        "answer": "6 3 10 5 16 8 4 2 1",
        "keywords": ["6 3 10 5 16 8 4 2 1"],
        "explanation": "6→3→10→5→16→8→4→2→1.",
    },
    {
        "id": "d-boot-missing",
        "module_id": "bootcamp",
        "title": "Missing ticket",
        "type": "code",
        "rating": 800,
        "source": {"title": "CSES Missing Number (skill)", "url": "https://cses.fi/problemset/task/1083"},
        "text": "First line: n (2 ≤ n ≤ 200). Second line: n−1 distinct integers in 1..n. Print the missing one.",
        "sample": {"stdin": "5\n2 3 1 5\n", "stdout": "4\n"},
        "starter": "n = int(input())\na = list(map(int, input().split()))\n# print the missing number in 1..n\n",
        "tests": [
            {"stdin": "5\n2 3 1 5\n", "stdout": "4\n"},
            {"stdin": "2\n1\n", "stdout": "2\n", "hidden": True},
            {"stdin": "4\n4 1 3\n", "stdout": "2\n", "hidden": True},
        ],
        "explanation": "xor 1..n with the list, or sum n(n+1)/2 minus the given sum.",
    },
    # --- Implementation ---
    {
        "id": "d-impl-run",
        "module_id": "impl",
        "title": "Longest run",
        "type": "code",
        "rating": 800,
        "source": {"title": "CSES Repetitions (skill)", "url": "https://cses.fi/problemset/task/1069"},
        "text": "Read one string s of uppercase letters (1 ≤ |s| ≤ 200). Print the length of the longest substring of identical characters.",
        "sample": {"stdin": "ATTCGGGA\n", "stdout": "3\n"},
        "starter": "s = input().strip()\n# print the longest run of the same letter\n",
        "tests": [
            {"stdin": "ATTCGGGA\n", "stdout": "3\n"},
            {"stdin": "AAAA\n", "stdout": "4\n"},
            {"stdin": "ABC\n", "stdout": "1\n", "hidden": True},
            {"stdin": "ABBBA\n", "stdout": "3\n", "hidden": True},
        ],
        "explanation": "Scan once, reset the current run when the letter changes.",
    },
    {
        "id": "d-impl-inc",
        "module_id": "impl",
        "title": "Make it non-decreasing",
        "type": "short",
        "rating": 900,
        "source": {"title": "CSES Increasing Array (skill)", "url": "https://cses.fi/problemset/task/1094"},
        "text": "You may increase any element by 1 any number of times. Array: 3 2 5 1 7. Minimum total increases so it becomes non-decreasing?",
        "answer": "5",
        "keywords": ["5"],
        "explanation": "3,2→need +1 to 3; 5 ok; 1→need +4 to 5; 7 ok. Total 5.",
    },
    {
        "id": "d-impl-fence",
        "module_id": "impl",
        "title": "Who stoops",
        "type": "code",
        "rating": 800,
        "source": {"title": "USACO Guide — Ad Hoc", "url": "https://usaco.guide/bronze/ad-hoc"},
        "text": "Line 1: n h. Line 2: n heights. A person of height > h needs width 2, else 1. Print total width.",
        "sample": {"stdin": "3 7\n4 9 7\n", "stdout": "4\n"},
        "starter": "n, h = map(int, input().split())\na = list(map(int, input().split()))\n",
        "tests": [
            {"stdin": "3 7\n4 9 7\n", "stdout": "4\n"},
            {"stdin": "1 1\n1\n", "stdout": "1\n", "hidden": True},
            {"stdin": "2 5\n6 6\n", "stdout": "4\n", "hidden": True},
        ],
        "explanation": "sum 2 if a_i > h else 1.",
    },
    {
        "id": "d-impl-candies",
        "module_id": "impl",
        "title": "Fair split of n",
        "type": "mcq",
        "rating": 800,
        "source": {"title": "USACO Guide — Ad Hoc", "url": "https://usaco.guide/bronze/ad-hoc"},
        "text": "You have n candies, n ≥ 1. You give some positive number to A and the rest to B, A gets strictly more than B, and n = A+B. How many ways, as a formula?",
        "options": ["n//2", "(n-1)//2", "n-1", "n*(n-1)/2"],
        "answer": "(n-1)//2",
        "explanation": "A from floor(n/2)+1 to n-1. Count is (n-1)//2.",
    },
    # --- Math ---
    {
        "id": "d-math-gcd",
        "module_id": "math",
        "title": "Euclid",
        "type": "short",
        "rating": 900,
        "source": {"title": "CP-Algorithms — Euclidean algorithm", "url": "https://cp-algorithms.com/algebra/euclid-algorithm.html"},
        "text": "gcd(48, 18) = ?",
        "answer": "6",
        "keywords": ["6"],
        "explanation": "48 = 2·18 + 12; 18 = 1·12 + 6; 12 = 2·6 + 0.",
    },
    {
        "id": "d-math-binpow",
        "module_id": "math",
        "title": "Last digits of a power",
        "type": "short",
        "rating": 900,
        "source": {"title": "CP-Algorithms — Binary exponentiation", "url": "https://cp-algorithms.com/algebra/binary-exp.html"},
        "text": "Compute 2^10 mod 1_000_000_007. (Just the integer.)",
        "answer": "1024",
        "keywords": ["1024"],
        "explanation": "2^10 = 1024, already smaller than the mod.",
    },
    {
        "id": "d-math-zeros",
        "module_id": "math",
        "title": "Trailing zeros",
        "type": "short",
        "rating": 1000,
        "source": {"title": "CSES Trailing Zeros / CPH Ch. 21", "url": "https://cses.fi/problemset/task/1618"},
        "text": "How many trailing zeros does 25! have?",
        "answer": "6",
        "keywords": ["6"],
        "explanation": "floor(25/5)+floor(25/25)=5+1=6.",
    },
    {
        "id": "d-math-sieve",
        "module_id": "math",
        "title": "Almost two primes",
        "type": "code",
        "rating": 900,
        "source": {"title": "CP-Algorithms — Sieve", "url": "https://cp-algorithms.com/algebra/sieve-of-eratosthenes.html"},
        "text": "Read n (1 ≤ n ≤ 50). Print how many integers in 1..n have exactly two distinct prime factors (e.g. 6=2·3 counts, 12=2^2·3 counts, 8=2^3 does not).",
        "sample": {"stdin": "10\n", "stdout": "2\n"},
        "starter": "n = int(input())\n# 6 and 10 in 1..10 → 2\n",
        "tests": [
            {"stdin": "10\n", "stdout": "2\n"},
            {"stdin": "1\n", "stdout": "0\n", "hidden": True},
            {"stdin": "30\n", "stdout": "12\n", "hidden": True},
        ],
        "explanation": "Sieve smallest prime factor, count distinct primes in the factorisation.",
    },
    {
        "id": "d-math-piles",
        "module_id": "math",
        "title": "Two piles",
        "type": "mcq",
        "rating": 1000,
        "source": {"title": "CSES Coin Piles (skill)", "url": "https://cses.fi/problemset/task/1754"},
        "text": "Piles a,b. A move removes 1 from one pile and 2 from the other. Can (4,2) be emptied?",
        "options": ["Yes", "No"],
        "answer": "Yes",
        "explanation": "Need a+b divisible by 3 and neither pile more than twice the other. 6÷3=2, 4 ≤ 2·2.",
    },
    # --- Greedy ---
    {
        "id": "d-greedy-movies",
        "module_id": "greedy",
        "title": "Pick the films",
        "type": "mcq",
        "rating": 1200,
        "source": {"title": "USACO Guide — Greedy with sorting", "url": "https://usaco.guide/silver/greedy-sorting"},
        "text": "Intervals (start,end): (1,4), (3,5), (0,6), (5,7), (3,8), (5,9), (6,10), (8,11), (8,12), (2,13), (12,14). Greedy: always take the one that finishes first among those that start after you are free. How many films?",
        "options": ["3", "4", "5", "6"],
        "answer": "4",
        "explanation": "Classic activity selection: (1,4), (5,7), (8,11), (12,14) — four.",
    },
    {
        "id": "d-greedy-kadane",
        "module_id": "greedy",
        "title": "Best subarray",
        "type": "short",
        "rating": 1200,
        "source": {"title": "CSES Maximum Subarray Sum / Kadane", "url": "https://cses.fi/problemset/task/1643"},
        "text": "Maximum subarray sum of [1, −2, 3, −1, 2]?",
        "answer": "4",
        "keywords": ["4"],
        "explanation": "3 + −1 + 2 = 4.",
    },
    {
        "id": "d-greedy-distinct",
        "module_id": "greedy",
        "title": "How many distinct",
        "type": "code",
        "rating": 800,
        "source": {"title": "CSES Distinct Numbers", "url": "https://cses.fi/problemset/task/1621"},
        "text": "Line 1: n. Line 2: n integers. Print how many distinct values.",
        "sample": {"stdin": "5\n2 3 2 2 3\n", "stdout": "2\n"},
        "starter": "n = int(input())\na = list(map(int, input().split()))\n",
        "tests": [
            {"stdin": "5\n2 3 2 2 3\n", "stdout": "2\n"},
            {"stdin": "1\n0\n", "stdout": "1\n", "hidden": True},
            {"stdin": "4\n1 1 1 1\n", "stdout": "1\n", "hidden": True},
        ],
        "explanation": "set(a) or sort and unique.",
    },
    {
        "id": "d-greedy-median",
        "module_id": "greedy",
        "title": "Meeting point",
        "type": "short",
        "rating": 1200,
        "source": {"title": "CSES Stick Lengths (skill)", "url": "https://cses.fi/problemset/task/1074"},
        "text": "Move each stick to the same length; cost is |x − a_i|. Sticks 1 2 9. Best common length and total cost? Write length then cost, like 2 8.",
        "answer": "2 8",
        "keywords": ["2 8", "2, 8"],
        "explanation": "Median of 1,2,9 is 2. |1−2|+|2−2|+|9−2|=8.",
    },
    # --- Search ---
    {
        "id": "d-search-mono",
        "module_id": "search",
        "title": "First true",
        "type": "short",
        "rating": 1100,
        "source": {"title": "CF EDU — Binary Search", "url": "https://codeforces.com/edu/course/2/lesson/6"},
        "text": "Array of predicates F F F T T T T (0-index). What index does lower_bound for the first True return?",
        "answer": "3",
        "keywords": ["3"],
        "explanation": "First T is index 3.",
    },
    {
        "id": "d-search-answer",
        "module_id": "search",
        "title": "Search on the answer",
        "type": "mcq",
        "rating": 1400,
        "source": {"title": "USACO Guide — Binary search on the answer", "url": "https://usaco.guide/silver/binary-search"},
        "text": "You need the minimum time T so that k machines with times t_i produce at least n items (each machine makes floor(T/t_i) items). What do you binary-search?",
        "options": ["The machine index", "T, checking if production(T) ≥ n", "n, checking if T is prime", "The gcd of t_i"],
        "answer": "T, checking if production(T) ≥ n",
        "explanation": "Monotonic in T: more time never produces fewer items. Classic Factory Machines.",
    },
    {
        "id": "d-search-drink",
        "module_id": "search",
        "title": "How many shops",
        "type": "code",
        "rating": 1100,
        "source": {"title": "CP-Algorithms — Binary search", "url": "https://cp-algorithms.com/num_methods/binary_search.html"},
        "text": "Line 1: n. Line 2: n shop prices. Line 3: q. Next q lines: coins. For each query print how many shops have price ≤ coins. n,q ≤ 200.",
        "sample": {"stdin": "5\n3 10 8 6 11\n4\n1\n10\n3\n11\n", "stdout": "0\n4\n1\n5\n"},
        "starter": "n = int(input())\np = list(map(int, input().split()))\nq = int(input())\n",
        "tests": [
            {"stdin": "5\n3 10 8 6 11\n4\n1\n10\n3\n11\n", "stdout": "0\n4\n1\n5\n"},
            {"stdin": "1\n5\n2\n4\n5\n", "stdout": "0\n1\n", "hidden": True},
        ],
        "explanation": "Sort prices, upper_bound for each query.",
    },
    # --- Prefix ---
    {
        "id": "d-pref-sum",
        "module_id": "prefix",
        "title": "Range in O(1)",
        "type": "short",
        "rating": 900,
        "source": {"title": "USACO Guide — Prefix sums", "url": "https://usaco.guide/silver/prefix-sums"},
        "text": "a = [2, 3, 7, 5, 1]. Prefix S[0]=0, S[k]=a[0]+…+a[k-1]. Sum of a[1..3] inclusive (3+7+5) using S?",
        "answer": "15",
        "keywords": ["15", "s[4]-s[1]"],
        "explanation": "S = [0,2,5,12,17,18]. S[4]−S[1]=17−2=15.",
    },
    {
        "id": "d-pref-code",
        "module_id": "prefix",
        "title": "Static range sums",
        "type": "code",
        "rating": 900,
        "source": {"title": "CSES Static Range Sum Queries (skill)", "url": "https://cses.fi/problemset/task/1646"},
        "text": "Line 1: n q. Line 2: n integers a1..an (1-index). Then q lines l r. Print a[l]+…+a[r] each query.",
        "sample": {"stdin": "4 3\n1 2 3 4\n1 2\n2 4\n1 4\n", "stdout": "3\n9\n10\n"},
        "starter": "n, q = map(int, input().split())\na = list(map(int, input().split()))\n",
        "tests": [
            {"stdin": "4 3\n1 2 3 4\n1 2\n2 4\n1 4\n", "stdout": "3\n9\n10\n"},
            {"stdin": "1 1\n9\n1 1\n", "stdout": "9\n", "hidden": True},
        ],
        "explanation": "Build prefix, answer S[r]−S[l−1].",
    },
    {
        "id": "d-pref-diff",
        "module_id": "prefix",
        "title": "Difference array",
        "type": "mcq",
        "rating": 1400,
        "source": {"title": "USACO Guide — More prefix sums", "url": "https://usaco.guide/silver/more-prefix-sums"},
        "text": "To add +v on index range [l,r] (1-index) using a difference array d, you do:",
        "options": [
            "d[l]+=v; d[r]+=v",
            "d[l]+=v; d[r+1]-=v",
            "d[l]-=v; d[r]+=v",
            "d[1]+=v",
        ],
        "answer": "d[l]+=v; d[r+1]-=v",
        "explanation": "Prefix of d reconstructs the array. The −v at r+1 stops the +v.",
    },
    # --- Graphs I ---
    {
        "id": "d-g1-bfsdfs",
        "module_id": "graphs1",
        "title": "Which walk",
        "type": "mcq",
        "rating": 1200,
        "source": {"title": "CP-Algorithms — BFS", "url": "https://cp-algorithms.com/graph/breadth-first-search.html"},
        "text": "Unweighted graph, shortest path in number of edges from s to t. Use:",
        "options": ["DFS only", "BFS from s", "Dijkstra with random weights", "Toposort"],
        "answer": "BFS from s",
        "explanation": "BFS layers are exact distances in an unweighted graph.",
    },
    {
        "id": "d-g1-comp",
        "module_id": "graphs1",
        "title": "Components",
        "type": "short",
        "rating": 1200,
        "source": {"title": "CSES Building Roads (skill)", "url": "https://cses.fi/problemset/task/1666"},
        "text": "n=6 nodes, edges 1-2, 2-3, 4-5. How many connected components? How many new roads to connect the whole graph?",
        "answer": "3 2",
        "keywords": ["3 2", "3 components", "2 roads"],
        "explanation": "{1,2,3}, {4,5}, {6}. Need 2 edges to link 3 components.",
    },
    {
        "id": "d-g1-bip",
        "module_id": "graphs1",
        "title": "Two colours",
        "type": "mcq",
        "rating": 1300,
        "source": {"title": "CSES Building Teams / bipartite", "url": "https://cses.fi/problemset/task/1668"},
        "text": "A triangle (3-cycle) is bipartite?",
        "options": ["Yes", "No"],
        "answer": "No",
        "explanation": "Odd cycle ⇒ not 2-colourable.",
    },
    {
        "id": "d-g1-code",
        "module_id": "graphs1",
        "title": "Count components",
        "type": "code",
        "rating": 1200,
        "source": {"title": "USACO Guide — Graph traversal", "url": "https://usaco.guide/silver/graph-traversal"},
        "text": "Line 1: n m. Then m lines u v (1-index, undirected). Print number of connected components.",
        "sample": {"stdin": "6 3\n1 2\n2 3\n4 5\n", "stdout": "3\n"},
        "starter": "n, m = map(int, input().split())\ng = [[] for _ in range(n + 1)]\nfor _ in range(m):\n    u, v = map(int, input().split())\n    g[u].append(v)\n    g[v].append(u)\n",
        "tests": [
            {"stdin": "6 3\n1 2\n2 3\n4 5\n", "stdout": "3\n"},
            {"stdin": "3 0\n", "stdout": "3\n", "hidden": True},
            {"stdin": "4 3\n1 2\n2 3\n3 4\n", "stdout": "1\n", "hidden": True},
        ],
        "explanation": "DFS/BFS from every unvisited node.",
    },
    # --- Graphs II ---
    {
        "id": "d-g2-dij",
        "module_id": "graphs2",
        "title": "When Dijkstra",
        "type": "mcq",
        "rating": 1500,
        "source": {"title": "CP-Algorithms — Dijkstra", "url": "https://cp-algorithms.com/graph/dijkstra.html"},
        "text": "Non-negative edge weights. Fastest known practical single-source shortest paths on a sparse graph?",
        "options": ["Bellman–Ford always", "Dijkstra + heap", "Plain BFS ignoring weights", "Floyd–Warshall only"],
        "answer": "Dijkstra + heap",
        "explanation": "BFS ignores weights. Bellman–Ford handles negatives but is slower. Floyd is all-pairs.",
    },
    {
        "id": "d-g2-neg",
        "module_id": "graphs2",
        "title": "Negative edge",
        "type": "mcq",
        "rating": 1600,
        "source": {"title": "CP-Algorithms — Bellman–Ford", "url": "https://cp-algorithms.com/graph/bellman_ford.html"},
        "text": "One edge has weight −3, all others positive, no negative cycle. Dijkstra (as usually coded with a visited[] flag) is:",
        "options": ["Always correct", "May be wrong; use Bellman–Ford / potential reduction", "Always infinite loop"],
        "answer": "May be wrong; use Bellman–Ford / potential reduction",
        "explanation": "Standard Dijkstra assumes non-negative weights.",
    },
    {
        "id": "d-g2-dsu",
        "module_id": "graphs2",
        "title": "Union-find",
        "type": "short",
        "rating": 1400,
        "source": {"title": "CP-Algorithms — DSU", "url": "https://cp-algorithms.com/data_structures/disjoint_set_union.html"},
        "text": "Start with 4 nodes. union(1,2), union(3,4), union(2,3). Are 1 and 4 in the same set? Answer yes or no.",
        "answer": "yes",
        "keywords": ["yes", "same"],
        "explanation": "All four merge into one component.",
    },
    # --- DP ---
    {
        "id": "d-dp-knap",
        "module_id": "dp",
        "title": "0/1 knapsack step",
        "type": "mcq",
        "rating": 1400,
        "source": {"title": "CP-Algorithms — Knapsack", "url": "https://cp-algorithms.com/dynamic_programming/knapsack.html"},
        "text": "dp[w] = best value with capacity w. Item value v, weight w_i. The correct in-place update order is:",
        "options": [
            "for w from 0 to W: dp[w] = max(dp[w], dp[w-w_i]+v)",
            "for w from W down to w_i: dp[w] = max(dp[w], dp[w-w_i]+v)",
            "dp[w_i] += v",
            "sort items by v/w only",
        ],
        "answer": "for w from W down to w_i: dp[w] = max(dp[w], dp[w-w_i]+v)",
        "explanation": "Going downward uses each item at most once. Upward would reuse it (unbounded).",
    },
    {
        "id": "d-dp-coins",
        "module_id": "dp",
        "title": "Min coins",
        "type": "short",
        "rating": 1400,
        "source": {"title": "CSES Minimizing Coins (skill)", "url": "https://cses.fi/problemset/task/1634"},
        "text": "Coins {1, 5, 7}, make 11. Minimum number of coins? (unlimited supply)",
        "answer": "3",
        "keywords": ["3"],
        "explanation": "7+1+1+… is 5 coins; 5+5+1=3; 7+...? 7+5−1 no. 5+5+1 = 3.",
    },
    {
        "id": "d-dp-dice",
        "module_id": "dp",
        "title": "Dice ways",
        "type": "code",
        "rating": 1200,
        "source": {"title": "CSES Dice Combinations (skill)", "url": "https://cses.fi/problemset/task/1633"},
        "text": "Read n (1 ≤ n ≤ 30). Number of ordered ways to write n as a sum of dice faces in {1..6}. Print modulo 10**9+7.",
        "sample": {"stdin": "3\n", "stdout": "4\n"},
        "starter": "MOD = 10**9 + 7\nn = int(input())\n",
        "tests": [
            {"stdin": "3\n", "stdout": "4\n"},
            {"stdin": "1\n", "stdout": "1\n"},
            {"stdin": "4\n", "stdout": "8\n", "hidden": True},
        ],
        "explanation": "dp[0]=1; dp[x] += dp[x-f] for f=1..6. 3: 1+1+1, 1+2, 2+1, 3 → 4.",
    },
    {
        "id": "d-dp-frog",
        "module_id": "dp",
        "title": "Frog 1",
        "type": "short",
        "rating": 1200,
        "source": {"title": "AtCoder DP contest — Frog 1", "url": "https://atcoder.jp/contests/dp/tasks/dp_a"},
        "text": "Heights 10 30 40 20. Cost |h_i−h_j| to jump i→i+1 or i+2. Min cost 1→n?",
        "answer": "30",
        "keywords": ["30"],
        "explanation": "10→30→20 costs |20|+|10|=30, better than going via 40.",
    },
    # --- Trees / strings ---
    {
        "id": "d-ts-diam",
        "module_id": "trees-str",
        "title": "Tree diameter trick",
        "type": "mcq",
        "rating": 1400,
        "source": {"title": "CSES Tree Diameter / USACO Guide", "url": "https://usaco.guide/gold/all-roots"},
        "text": "To find the diameter of a tree: BFS/DFS from an arbitrary node to a farthest node u, then from u to a farthest node v. The diameter is:",
        "options": ["deg(u)", "dist(u,v)", "n-1 always", "the centroid"],
        "answer": "dist(u,v)",
        "explanation": "Two BFS. Standard tree diameter.",
    },
    {
        "id": "d-ts-hash",
        "module_id": "trees-str",
        "title": "Why hash strings",
        "type": "mcq",
        "rating": 1600,
        "source": {"title": "CP-Algorithms — String hashing", "url": "https://cp-algorithms.com/string/string-hashing.html"},
        "text": "Polynomial rolling hash lets you compare two substrings in:",
        "options": ["O(|s|)", "O(1) after O(n) prep (with tiny collision risk)", "O(n log n) always", "O(n²)"],
        "answer": "O(1) after O(n) prep (with tiny collision risk)",
        "explanation": "Prefix hashes + modular inverse / pow of base.",
    },
    {
        "id": "d-ts-kmp",
        "module_id": "trees-str",
        "title": "Prefix function",
        "type": "short",
        "rating": 1400,
        "source": {"title": "CP-Algorithms — Prefix function (KMP)", "url": "https://cp-algorithms.com/string/prefix-function.html"},
        "text": "Prefix function π of \"ababab\". Write the 6 values space-separated.",
        "answer": "0 0 1 2 3 4",
        "keywords": ["0 0 1 2 3 4"],
        "explanation": "Longest proper prefix that is also suffix at each position.",
    },
]

from camp.drills_extra import EXTRA_DRILLS

DRILLS.extend(EXTRA_DRILLS)


def drill_by_id(qid: str) -> dict | None:
    return next((d for d in DRILLS if d["id"] == qid), None)


def drills_for_module(mid: str) -> list[dict]:
    return [d for d in DRILLS if d["module_id"] == mid]


def public_drill(d: dict) -> dict:
    """Drop hidden test stdout before sending to the browser."""
    out = {k: v for k, v in d.items() if k != "tests"}
    if d.get("tests"):
        out["sample"] = d.get("sample") or next(
            ({"stdin": t["stdin"], "stdout": t["stdout"]} for t in d["tests"] if not t.get("hidden")),
            None,
        )
    return out


def pick_drills(module_ids: list[str], solved: dict, learner: dict | None, n: int = 5) -> list[dict]:
    pool = [d for d in DRILLS if d["module_id"] in module_ids]
    if not pool:
        pool = list(DRILLS)
    open_d = [d for d in pool if d["id"] not in solved] or pool

    def score(d: dict) -> float:
        if not learner:
            return float(d.get("rating") or 1000)
        node = learner["modules"].get(d["module_id"])
        if not node:
            return 0.0
        skill = effective_skill(node)
        p = expected_score(skill, float(d.get("rating") or 1100))
        return -abs(p - 0.70)

    ranked = sorted(open_d, key=score)
    # Keep a mix of types if possible.
    picked: list[dict] = []
    used_mod = set()
    for d in ranked:
        if len(picked) >= n:
            break
        if d["module_id"] in used_mod and len(picked) < n - 1 and len({x["module_id"] for x in ranked}) > 1:
            continue
        picked.append(d)
        used_mod.add(d["module_id"])
    for d in ranked:
        if len(picked) >= n:
            break
        if d not in picked:
            picked.append(d)
    return picked[:n]
