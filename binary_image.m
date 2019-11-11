I = ones(10,10)
I(3,3) = 0
I(3,7) = 0
I(7,3:7) = 0


imwrite(I,'sm.png')