!Purpose: to create .SOL file dynamically
!Author:  Amor VM Ines
!Institute:	Michigan State University
!Date: 2/28/2020
!Reference: Han,Ines and Koo (2019).Environmental Modelling and Software.119:70-83.

program dotSolAPI2

!Algorithm========
!read the CSV file from Josue's python code

!from PTF:
!estimate SLLL
!estimate SDUL
!estimate SSAT
!estimate SSKS

!fill up values of other .SOL variables

!conditionals: ???
!rooting depth (deep, medium, shallow)?
!fertility (high, medium, low)?	  !not used in this application

!write .SOL
!Algorithm========


!read the CSV file from Josue's python code
!SBDM - bulk density
!SLCL - clay fraction
!SLOC - organic carbon
!SLSN - sand fraction 
!SLSI - silt fraction; 100-SLCL-SLSN

integer:: iost, i,j,k
character(len=80):: line1
character*9:: what_texture,USDA
character*1:: What_tex_4HC,HC

real,dimension(6):: SBDM,SLCL,SLOC,SAND,SLSI,lati,long,depthi
real,dimension(6):: Theta33t,SOM,SDUL
real,dimension(6):: Theta15t,SLLL,Thetas_33t,Thetas_33,SSAT
real,dimension(6):: B,lamda,SSKS
real,dimension(6):: SRGF_s,SRGF_m,SRGF_d !shallow,medium,deep roots
real,dimension(6):: SLNI_s,SLNI_m,SLNI_d !low,medium,high fertility
real,dimension(6):: SLB
character(len=5),dimension(6)::SLMH 
real,dimension(6):: SRGF, SLNI,SLCF,SLHW,SLHB,SCEC,SADC !note: SLCF is SAND
real:: SALB,SLU1,SLDR,SLRO,SLNF,SLPF
character(len=5):: SCOM,SMHB,SMPX,SMKE

!clay soils
real:: SALB_clay,SLU1_clay,SLDR_clay,SLRO_clay,SLNF_clay,SLPF_clay
character(len=5):: SCOM_clay,SMHB_clay,SMPX_clay,SMKE_clay
!sand soils
real:: SALB_sand,SLU1_sand,SLDR_sand,SLRO_sand,SLNF_sand,SLPF_sand
character(len=5):: SCOM_sand,SMHB_sand,SMPX_sand,SMKE_sand
!loam soils
real:: SALB_loam,SLU1_loam,SLDR_loam,SLRO_loam,SLNF_loam,SLPF_loam
character(len=5):: SCOM_loam,SMHB_loam,SMPX_loam,SMKE_loam

character(len=2):: C_ID         
real:: lat, lon, depth
character(len=10):: rep_HCID

character(len=50):: SLSOUR,SLTXS,SLDESC
character(len=20):: temp_ID
character(len=10):: soil_ID
real:: SLDP

    !for the command line
    character(len=90)   :: fparam
    integer(kind=2)     :: n1,status
    character(len=90)   :: buf

    logical:: EXISTS

!rooting depth
!SRGF_shallow
data SRGF_s /1.,1.0,0.65,0.,0.,0./	  !0-30 cm
!SRGF_medium
data SRGF_m /1.0,1.0,0.65,0.38,0.,0./ !30-60 cm
!SRGF_deep
data SRGF_d /1.0,1.0,0.65,0.38,0.22,0.08/ !60-200 cm

!soil fertility	(not used in this application)
!SLNI_low
data SLNI_s /0.,0.,0.,0.,0.,0./
!SLNI_medium
data SLNI_m /0.,0.,0.,0.,0.,0./
!SLNI_high
data SLNI_d /0.,0.,0.,0.,0.,0./

!soil depth
data SLB /1.,10.,30.,60.,100.,200./

!soil horizon
data SLMH /'A','A','AB','BA','B','BC'/

!initialize variables
SLLL=-99.
SDUL=-99.
SSAT=-99.
SRGF=-99.
SSKS=-99.
SBDM=-99.
SLOC=-99.
SLCL=-99.
SLSI=-99. 
SLCF=-99.
SLNI=-99.
SLHW=-99.  
SLHB=-99.  
SCEC=-99.
SADC=-99.
SCOM='-99.0'
SALB=-99.
SLU1=-99.
SLDR=-99.
SLRO=-99.
SLNF=-99.
SLPF=-99.
SMHB='-99.0'
SMPX='-99.0'
SMKE='-99.0'

lat=-99.
lon=-99.
SLDP=-99.

!loam soils
SCOM_loam='BK'
SALB_loam=0.10
SLU1_loam=6.00
SLDR_loam=0.50
SLRO_loam=75.00
SLNF_loam=1.00
SLPF_loam=1.00
SMHB_loam='SA001'
SMPX_loam='SA001'
SMKE_loam='SA001'

!clay soils	   
SCOM_clay='BK'
SALB_clay=0.05
SLU1_clay=8.00
SLDR_clay=0.20
SLRO_clay=85.00
SLNF_clay=1.00
SLPF_clay=1.00
SMHB_clay='SA001'
SMPX_clay='SA001'
SMKE_clay='SA001'

!sand soils		  
SCOM_sand='BK'
SALB_sand=0.15
SLU1_sand=4.00
SLDR_sand=0.75
SLRO_sand=65.00
SLNF_sand=1.00
SLPF_sand=1.00
SMHB_sand='SA001'
SMPX_sand='SA001'
SMKE_sand='SA001'


    !retrieves command line using module dflib.f90
!    n1=0
!    do while(n1 .le. 1)
!        call getarg(n1,buf,status)
!        !error flag for command line
!        if(status == -1)then
!            write(6,*)'error in the command line:'
!            write(6,*)'usage: <command> <file1>'
!            write(6,*)'<file1>: parameter file - where data for simulations are given'
!            pause;
!            ! stop
!        endif
!        if(n1==1)fparam=buf
!        n1=n1+1
!    enddo
    !----end command line syntax----- 

!! gfortran getarg() by Honda 2019-12-28
if ( iargc() .NE. 1 ) then
	!write(6,*)'ERROR in the command line:'
	!write(6,*)'USAGE: <Command> <file1>'
	!write(6,*)'<file1>: Parameter file - where data for simulations are given'
	stop
endif
n1=1
call getarg(n1,buf)
fparam=buf

open (unit=10, file=trim(fparam),status='old',iostat=iost)
if(iost .ne. 0)  stop 'No data in asc file, pls check file:####.asc'

!reads header 
read(10,'(a)')line1 

do i=1,6 !6 number of soil layers
	read(10,*) SBDM(i),SLCL(i),SLOC(i),SAND(i),lati(i),long(i),depthi(i) !new asc file
!	read(10,*) SBDM(i),SLCL(i),SLOC(i),SAND(i) !old asc file
	SLSI(i) = 100 - (SLCL(i) + SAND(i))
enddo 

close(10)

!debug
!do i=1,6 !6 number of soil layers
!	!write(6,*) SBDM(i),SLCL(i),SLOC(i),SAND(i),SLSI(i)
!enddo 

!estimating soil SDUL,SLLL

SOM = 2*SLOC   !instead of 1.72

!print*,(SOM(i),i=1,6)


!transforming to PTF units
SLCL=SLCL/100.
SAND=SAND/100.
SOM=SOM/2.
!SOM=SOM/1000.

!SDUL - drained upper limit
Theta33t=-0.251*SAND+0.195*SLCL+0.011*SOM+0.006*SAND*SOM-0.027*SLCL*SOM+0.452*SAND*SLCL+0.299
SDUL=Theta33t+1.283*Theta33t*Theta33t-0.374*Theta33t-0.015

!SDLL - drained lower limit 
Theta15t=-0.024*SAND+0.487*SLCL+0.006*SOM+0.005*SAND*SOM-0.013*SLCL*SOM+0.068*SAND*SLCL+0.031
SLLL=Theta15t+0.14*Theta15t-0.02

!SSAT - saturated soil moisture
Thetas_33t=0.278*SAND+0.034*SLCL+0.022*SOM-0.018*SAND*SOM-0.027*SLCL*SOM-0.584*SAND*SLCL+0.078
Thetas_33=Thetas_33t+0.636*Thetas_33t-0.107
SSAT=SDUL+Thetas_33-0.097*SAND+0.043

!SSKS - saturated hydraulic conductivity
B=(log(1500.0)-log(33.0))/(log(SDUL)-log(SLLL))
lamda=1/B
SSKS=1930*(SSAT-SDUL)**(3-lamda) ! mm/hr
SSKS=SSKS*0.1 ! cm/hr for DSSAT


!print*,'SDUL:',(SDUL(i),i=1,6)
!print*,'SLLL:',(SLLL(i),i=1,6)
!print*,'SSAT:',(SSAT(i),i=1,6)
!print*,'SSKS:',(SSKS(i),i=1,6)

!Whats the HC texture class?
!print*,SAND(1),SLCL(1)
!HC=What_tex_4HC(SAND(1), SLCL(1))

!What's the USDA class?
!USDA=what_texture(SAND(1), SLCL(1))

!putting back to DSSAT .SOL units
SLCL=SLCL*100.
SAND=SAND*100.
SOM=SOM/2.
!SOM=SOM/1000.
SLOC=SLOC/2.

!Whats the HC texture class?
!print*,SAND(1),SLCL(1)
HC=What_tex_4HC(SAND(1), SLCL(1))

!What's the USDA class?
USDA=what_texture(SAND(1), SLCL(1))


!root depth medium default
!SRGF=SRGF_m !will be dynamic
 
!SLCF=SAND
SLCF=-99.
SLNI=-99. !no fertility profile	SLNI_# not used yet
SLHW=-99.  
SLHB=-99.  
SCEC=-99.
SADC=-99.

!assigning some SOL properties if Sand, Clay or Loam form HC27.SOL
if(trim(HC) .eq. 'L')then
	SCOM=SCOM_loam
	SALB=SALB_loam
	SLU1=SLU1_loam
	SLDR=SLDR_loam
	SLRO=SLRO_loam
	SLNF=SLNF_loam
	SLPF=SLPF_loam
	SMHB=SMHB_loam
	SMPX=SMPX_loam
	SMKE=SMKE_loam
elseif(trim(HC) .eq. 'S')then
	SCOM=SCOM_sand
	SALB=SALB_sand
	SLU1=SLU1_sand
	SLDR=SLDR_sand
	SLRO=SLRO_sand
	SLNF=SLNF_sand
	SLPF=SLPF_sand
	SMHB=SMHB_sand
	SMPX=SMPX_sand
	SMKE=SMKE_sand
elseif(trim(HC) .eq. 'C')then
	SCOM=SCOM_clay
	SALB=SALB_clay
	SLU1=SLU1_clay
	SLDR=SLDR_clay
	SLRO=SLRO_clay
	SLNF=SLNF_clay
	SLPF=SLPF_clay
	SMHB=SMHB_clay
	SMPX=SMPX_clay
	SMKE=SMKE_clay
else   !default
	SCOM=SCOM_loam
	SALB=SALB_loam
	SLU1=SLU1_loam
	SLDR=SLDR_loam
	SLRO=SLRO_loam
	SLNF=SLNF_loam
	SLPF=SLPF_loam
	SMHB=SMHB_loam
	SMPX=SMPX_loam
	SMKE=SMKE_loam
endif

!SGRF assignment
if(depthi(1) .le. 300.)then
	SRGF=SRGF_s
elseif(depthi(1) .gt. 300. .and. depthi(1) .le. 600.)then
	SRGF=SRGF_m
elseif(depthi(1) .gt. 600. .and. depthi(1) .le. 200.)then
	SRGF=SRGF_d
else !default
	SRGF=SRGF_m
endif

!lat=-99.
!lon=-99.
!SLDP=-99.


!================
temp_ID='*TH_0000001' !can be automatic?
SLSOUR='THA'
SLTXS= trim(USDA) !;print*,trim(USDA) !'XOXO' !i will add what_tex.f90 and inpoly.f90 later
SLDP=200  !2m deep soil standard in soilgrids250m 
SLDESC='ISRIC soilgrids250m + HC27'

C_ID='TH'
lat = lati(1) !will be taken from argument/file .asc
lon	= long(1) !will be taken from argument/file .asc
rep_HCID='XOXOXO' !more informative later
!================

!writing .SOL

open(unit=300,file='TH.SOL',status='unknown')

!write(6,5040)trim(temp_ID),trim(SLSOUR),trim(SLTXS),int(SLDP),trim(SLDESC)
write(300,5040)trim(temp_ID),trim(SLSOUR),trim(SLTXS),int(SLDP),trim(SLDESC)
5040 FORMAT (A11, 2X, A5,3X,A9,1X,I5,1X,A27) !edited A25 to A27

!write(6,'(a)')'@SITE        COUNTRY          LAT     LONG SCS Family'
write(300,'(a)')'@SITE        COUNTRY          LAT     LONG SCS Family'

!write(6,5050) '-99',trim(C_ID),lat,lon,trim(SLTXS)
write(300,5050) '-99',trim(C_ID),lat,lon,trim(SLTXS)
5050 FORMAT (A4, 2X, A14,4X,2(F9.3),A15)

!write(6,'(a)')'@ SCOM  SALB  SLU1  SLDR  SLRO  SLNF  SLPF  SMHB  SMPX  SMKE'
write(300,'(a)')'@ SCOM  SALB  SLU1  SLDR  SLRO  SLNF  SLPF  SMHB  SMPX  SMKE'

!write(6,500) SCOM,SALB, SLU1, SLDR, SLRO, SLNF, SLPF,SMHB, SMPX, SMKE  
write(300,500) SCOM,SALB, SLU1, SLDR, SLRO, SLNF, SLPF,SMHB, SMPX, SMKE  
500  FORMAT (A6,6F6.2,3A6)

!write(6,'(a)')'@  SLB  SLMH  SLLL  SDUL  SSAT  SRGF  SSKS  SBDM  SLOC  SLCL  SLSI  SLCF  SLNI  SLHW  SLHB  SCEC  SADC' 
write(300,'(a)')'@  SLB  SLMH  SLLL  SDUL  SSAT  SRGF  SSKS  SBDM  SLOC  SLCL  SLSI  SLCF  SLNI  SLHW  SLHB  SCEC  SADC' 

do i=1,6 !because soilgrids250m data we have got 6 layers

!WRITE (6,5112) int(SLB(i)),SLMH(i),SLLL(i),SDUL(i),SSAT(i),SRGF(i),SSKS(i),SBDM(i), && SLOC(i),SLCL(i),SLSI(i),SLCF(i),SLNI(i),SLHW(i),SLHB(i),SCEC(i),SADC(i)

WRITE (300,5112) int(SLB(i)),SLMH(i),SLLL(i),SDUL(i),SSAT(i),SRGF(i),SSKS(i),SBDM(i), &
& SLOC(i),SLCL(i),SLSI(i),SLCF(i),SLNI(i),SLHW(i),SLHB(i),SCEC(i),SADC(i)

enddo

!5112  FORMAT (1X,I5,1X,A5,3(1X,F5.3),1X,F5.2,1X,F5.2,4(1X,F5.2),1X,F5.1,2(1X,F5.2),3(1X,F5.1)) !EJ(11/13/2014) make SSKS=-99
5112  FORMAT (1X,I5,1X,A5,3(1X,F5.3),1X,F5.2,1X,F5.2,4(1X,F5.2),1X,F5.1,2(1X,F5.1),3(1X,F5.1)) !EJ(11/13/2014) make SSKS=-99
5113  FORMAT (1X,I5,1X,A5,3(1X,F5.3),1X,F5.2,1X,F5.2,4(1X,F5.2),1X,F5.1,1X,F5.2,4(1X,F5.1)) !EJ(11/13/2014) make SSKS=-99
5114  FORMAT (1X,I5,1X,A5,3(1X,F5.1),1X,F5.1,3(1X,F5.1),1X,F5.1,1X,F5.1,2(1X,F5.1),4(1X,F5.1)) !when -99 exists

close(300)

end program dotSolAPI2
