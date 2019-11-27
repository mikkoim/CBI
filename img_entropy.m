I = imread('testi.png');
n = prod(size(I));

v = I(:);

showvec = @(v) imshow(reshape(v,[64,64]));
glcm = @(I) graycoprops(graycomatrix(I,'NumLevels',2));

vhat = circshift(v,1);

g = struct('Contrast',{},'Correlation',{},'Energy',{},'Homogeneity',{})

for i = 1:64
    vhat = vhat(randperm(n));
    Ihat = reshape(vhat,[64,64]);
    g(i) = glcm(Ihat)
    showvec(vhat);
end

g2 = struct('Contrast',{},'Correlation',{},'Energy',{},'Homogeneity',{})

for i = 1:64
    vhat = circshift(v,1);
    Ihat = reshape(vhat,[64,64]);
    g2(i) = glcm(Ihat)
    showvec(vhat);
end

plot([g.Contrast])
hold on
plot([g2.Contrast])