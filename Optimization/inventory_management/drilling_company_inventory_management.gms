

  Sets
       s   working areas  / a,b,c,d,e,f,g,h,j,k,l /
       i    required materials   /1,2,3,4,5,6/
       ;

  Parameters
   v(s,i)   space possesed by i materials under the s working area (m^3)
/  a.1  0.03
   a.2  0.01
   a.3  0.07
   a.4  0.01
   a.5  0.06
   a.6  0.08
   
   b.1  0.30
   b.2  0.03
   b.3  0.08
   
   c.1  0.3
   c.2  0.5
   c.3  1.5
   
   d.1  1.5
   d.2  0.1
   d.3  0.2
   
   e.1  0.5
   e.2  0.1
   e.3  0.5
   e.4  2.5
   
   f.1  0.2
   f.2  0.1
   
   g.1  5
   g.2  4
   
   h.1  1.8
   h.2  0.3
   h.3  0.1
   h.4  2
   h.5  0.08
   h.6  0.2
   
   j.1  0.02
   j.2  0.02
   j.3  0.02
   j.4  0.02
   
   k.1  2
   k.2  3
   k.3  1.8
   
   l.1  1.6
   l.2  0.06
   l.3  0.8  /
   
    t(s,i) waiting time for the missing material i under the working area of s (day)
/
   a.1  1
   a.2  1
   a.3  1
   a.4  2
   a.5  2
   a.6  2
   
   b.1  3
   b.2  1
   b.3  0.5
   
   c.1  1
   c.2  2
   c.3  3
   
   d.1  1
   d.2  2
   d.3  2
   
   e.1  4
   e.2  4
   e.3  4
   e.4  4
   
   f.1  4
   f.2  4
   
   g.1  3
   g.2  3
   
   h.1  15
   h.2  10
   h.3  14
   h.4  15
   h.5  7
   h.6  7
   
   j.1  0.5
   j.2  0.5
   j.3  1
   j.4  1
   
   k.1  3
   k.2  2
   k.3  3
   
   l.1  4
   l.2  2
   l.3  2
   /
   
    n(s,i) price of one package of i material under the s working area(TL)
/
   a.1  1000
   a.2  1000
   a.3  1000
   a.4  5000
   a.5  10000
   a.6  10000
   
   b.1  8000
   b.2  2500
   b.3  2400
   
   c.1  4000
   c.2  1200
   c.3  25000
   
   d.1  8000
   d.2  5000
   d.3  5000
   
   e.1  3000
   e.2  1200
   e.3  7200
   e.4  8000
   
   f.1  6000
   f.2  1800
   
   g.1  52500
   g.2  42000
   
   h.1  100000
   h.2  300000
   h.3  8000
   h.4  30000
   h.5  20000
   h.6  50000
   
   j.1  500
   j.2  300
   j.3  700
   j.4  1000
   
   k.1  10000
   k.2  16000
   k.3  12500
   
   l.1  15000
   l.2  1200
   l.3  7000
    
/

;



  Positive Variable
  x(s,i)    number of package of i materials under the z working area
  P(s,i)    if a package supplied less than 3 and will be supplied on the process
  R(s,i)    if a package supplied more than 3
        ;
 
  Scalar
  u dailly profit recived from the production of ZT 250 Q8 (TL) /13900/
  y total space for the stocking of materials (m^3) /95/
  ;
  
       
  Variable
  z cost
  ;
  
Binary Variable
w(s,i);


  Equation
  wdef(s, i)
  supply_constraint(s, i)
  space_constraint(s)
  cost_function ;
  

  wdef(s,i).. w(s,i) =e= ifthen(n(s,i) > 1, 1, 0);
  supply_constraint(s, i)..     x(s,i) + P(s,i) - R(s,i) =e= 3*w(s,i) ;
  space_constraint(s).. sum((i), x(s, i) * t(s, i)) =l= y ;
  cost_function..         z  =e= sum((s,i), (x(s,i)+P(s,i))*n(s,i) + P(s,i)*t(s,i)*13900) ;
  


  Model final /all/ ;

  Solve final using mip minimazing z ;

  Display x.l,P.l ;

