# [**The falling speed of petals**](https://www.codewars.com/kata/5a0be7ea8ba914fc9c00006b)

## **Description:**
When it's spring Japanese cherries blossom, it's called "sakura" and it's admired a lot. The petals start to fall in late April.

Suppose that the falling speed of a petal is 5 centimeters per second (5 cm/s), and it takes 80 seconds for the petal to reach the ground from a certain branch.

Write a function that receives the speed (in cm/s) of a petal as input, and returns the time it takes for that petal to reach the ground **from the same branch**.

**Notes:**
- The movement of the petal is quite complicated, so in this case we can see the velocity as a constant during its falling.
- Pay attention to the data types.
- If the initial velocity is non-positive, the return value should be `0`

# **Solutions**

>
> [![img](https://cdn.iconscout.com/icon/free/png-512/free-c-icon-svg-png-download-226082.png?f=webp&w=24)](https://www.codewars.com/kata/5a0be7ea8ba914fc9c00006b/train/cpp)  
> ```cpp
> double SakuraFall(double v) {
>     if (v <= 0) return 0.0;
>     return 400.0 / v;
> }
> ```
> #
> [![img](https://cdn.iconscout.com/icon/free/png-512/free-csharp-icon-svg-png-download-1175241.png?f=webp&w=24)](https://www.codewars.com/kata/5a0be7ea8ba914fc9c00006b/train/csharp)
> ```cs
> public static class Kata
> {
>     public static double SakuraFall(double v)
>     {
>         if (v <= 0) return 0.0;
>         return 400.0 / v;
>     }
> }
> ```
> #
> [![img](https://cdn.iconscout.com/icon/free/png-512/free-julia-logo-icon-svg-png-download-2284963.png?f=webp&w=24)](https://www.codewars.com/kata/5a0be7ea8ba914fc9c00006b/train/julia)
> ```jl
> function sakura_fall(v)
>     if v <= 0
>         return 0.0
>     else
>         return 400.0 / v
>     end
> end
> ```
> #
> [![img](https://cdn.iconscout.com/icon/free/png-512/free-javascript-icon-svg-png-download-225993.png?f=webp&w=24)](https://www.codewars.com/kata/5a0be7ea8ba914fc9c00006b/train/javascript)
> ```js
> function sakuraFall(v) {
>   if (v <= 0) return 0;
>   return 400 / v;
> }
> ```
> #
> [![img](https://cdn.iconscout.com/icon/free/png-512/free-python-icon-svg-png-download-226051.png?f=webp&w=24)](https://www.codewars.com/kata/54bebed0d5b56c5b2600027f/train/python)
> ```py
> def sakura_fall(v):
>     if v <= 0:
>         return 0.0
>     return 400.0 / v
> ```
> #
> [![img](https://cdn.iconscout.com/icon/free/png-512/free-ruby-icon-svg-png-download-1175101.png?f=webp&w=24)](https://www.codewars.com/kata/54bebed0d5b56c5b2600027f/train/ruby)
> ```rb
> def sakura_fall(v)
>   return 0.0 if v <= 0
>   400.0 / v
> end
> ```
> #
> [![img](https://cdn.iconscout.com/icon/free/png-512/free-typescript-icon-svg-png-download-2945272.png?f=webp&w=24)](https://www.codewars.com/kata/54bebed0d5b56c5b2600027f/train/typescript)
> ```ts
> export function sakuraFall(v: number): number {
>   if (v <= 0) return 0;
>   return 400 / v;
> }
> ```
> #
>