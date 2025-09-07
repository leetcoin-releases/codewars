/*
Solution
*/
public static class Kata
{
    public static double SakuraFall(double v)
    {
        if (v <= 0) return 0.0;
        return 400.0 / v;
    }
}





/*
Sample Tests
*/
using NUnit.Framework;

[TestFixture]
public class SampleTests
{
    [Test]
    public void SampleTest()
    {
        Assert.That(
            Kata.SakuraFall(5),
            Is.EqualTo(80).Within(1e-6));
    }
}