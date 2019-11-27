I = imread('zambia.jpg');

B = rgb2gray(I);
B2 = imresize(B,[100,100]);
levels = 4;
thresh = multithresh(B2,levels);

B3 = uint8(imquantize(B2,thresh));
B3 = B3-1;
B4 = uint8( B3*(255/levels) );

imshow(B4)
imwrite(B4,'zambia_tresh.gif')
%% With dithering

I = imread('zambia.jpg');

B = rgb2gray(I);
B2 = imadjust(B,stretchlim(B),[]);
B3 = imresize(B2,[64,64]);

B4 = dither(B3);

imshow(B4)
imwrite(B4,'zambia_dither.gif')


%% Binary
I = imread('homer.jpg');
B = rgb2gray(I);
B2 = imresize(B,[64,64]);

BW = imbinarize(B2,graythresh(B2));
imshow(BW)

imwrite(BW, 'homer_bw.gif')
