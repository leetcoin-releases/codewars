/*
Solution
*/
double SakuraFall(double v) {
    if (v <= 0) return 0.0;
    return 400.0 / v;
}





/*
Sample Tests
*/
Describe(ExampleTest) {
    It(BasicTest) {
        Assert::That(SakuraFall(5), EqualsWithDelta(80, 1e-6));
    }
};