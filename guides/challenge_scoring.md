    # Challenge Scoring & Leaderboard

    ## Leaderboard

    Each challenge has its own leaderboard that ranks participants based on the **score** their solution achieves. The higher your score, the better your ranking!

    Participants can submit multiple times, and only their **highest-scoring solution** is used for the leaderboard. This encourages them to keep improving their work by making it not just more accurate, but also faster and more reliable.

    ![Leaderboard displaying the highest-scored submissions](https://d2lkyury6zu01n.cloudfront.net/images/leaderboard.png)
    *Leaderboard displaying the highest-scored submissions*

    After the deadline, the **top 3 positions** are preliminarily assigned to the highest-scoring submissions. However, these results are **subject to a manual review**. During this review, the challenge committee checks whether the solution meets all requirements. If it does not comply, it may be disqualified and the next highest-ranked submission will be reviewed in its place.

    To validate the result, the winning participant must provide their solution description. Other participants request to have their solution descriptions published, subject to review.

    Only submissions received before the deadline are considered for recognition on the official top 3 cards.

    ![Top 3 highest-scored solutions (submitted before the deadline)](https://d2lkyury6zu01n.cloudfront.net/images/winners.png)
    *Top 3 highest-scored solutions (submitted before the deadline)*

    📜 See the full [FHERMA Participant guide](https://fherma.io/how_it_works)

    ## What is the Score?

    The **score** reflects how good your solution is. It takes into account:

    - **Accuracy:** indicates how well the task is performed, using a relevant metric (e.g., accuracy, F1, RMSE).
    - **Processing time**: measures the average processing time per test case.
    - **Failures:** counts the number of test cases your solution fails to process (e.g., due to exceeding encryption noise, runtime errors, etc).

    The formula is:

    $$
    score =  f(r_f)(s_b - p(t)),
    $$

    ## Score Components

    Now let’s take a closer look at the key elements that make up the overall score.

    #### 1. Accuracy and Base Score

    This is the core measure of how well your solution performs according to the primary evaluation metric.

    $$
    s_b = s_t \cdot a
    $$

    - $a$ - accuracy of your solution (from 0 to 100), as defined by the primary metric.
    - $s_t$ - challenge-specific scaling factor (default is 10)

    This gives a maximum base score of 1000 when `a = 100` and `s_t = 10` .

    > Depending on the challenge, the primary metric could be accuracy, F1 score, recall, RMSE, or another relevant measure. Detailed information can be found in each challenge’s description.

    #### 2. Failures Penalty

    A coefficient applied if some test cases fail.

    $$
    f(r_f) = (1-r_f)^k: [0,1]
    $$

    - $r_{f}$ - failure rate `r_fails = n_fails/n_tests`
    - $k$ - exponent to control penalty strength (default is 3)

    If all test cases pass, $f(r_f)=1$ (no penalty). Otherwise, the score is reduced.

    #### 3. Time Penalty

    A deduction based on the average time your solution takes to process each test case.

    $$
    p(t)=\varepsilon \cdot\ln(1+\beta t_{avg}):[0, \inf)
    $$

    - $t_{avg}$ – average time to process one test case (in seconds)
    - $\varepsilon$ – time penalty factor (default is 3)
    - $\beta$ – time scaling parameter (default is 1)

    ## Example Calculation

    Suppose you submitted a model with:

    - 95% accuracy → `a = 95`
    - No failed test cases → `r_f = 0`
    - Average processing time per test: 1,000 seconds

    Then:

    - Base score with $s_t = 10$:
        
        $$
        s_b = s_t \cdot a = 10 \cdot 95 = 950
        $$
        
    - Failure penalty coefficient with $k = 3$:

    $$
    f(r_f) = (1-r_f)^k = (1 - 0)^3 = 1
    $$

    - Time penalty with $\varepsilon = 3$ and $\beta = 1$:

    $$
    p(t)=\varepsilon \cdot\ln(1+\beta t_{avg})=3⋅ln(1+10)=3⋅ln(11)≈3⋅2.398≈7.19
    $$

    - Final score:
        
        $$
        score =  f(r_f)(s_b - p(t)) = 1⋅(950−7.19)=942.81
        $$
        

    In summary, the final score reflects not only the quality of the solution but also its stability and efficiency. This allows for fair comparison among participants and encourages improvements across all key aspects.

    > The scoring formula may be expanded in the future to include additional factors such as memory usage or other relevant performance metrics.