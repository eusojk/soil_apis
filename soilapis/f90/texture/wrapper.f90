!this program will outputs the textural class given SAND and CLAY fractions

program	make_texture

real:: SAND,clay
character(len=9):: what_texture, soil_texture


    !for the command line
    character(len=32)   :: fparam,fparam2
    integer(kind=2)     :: n1,status
    character(len=32)   :: buf

    logical:: EXISTS


    !retrieves command line using module dflib.f90
!    n1=0
!    do while(n1 .le. 2)
!        call getarg(n1,buf,status)
!        !error flag for command line
!        if(status == -1)then
!            write(6,*)'error in the command line:'
!            write(6,*)'usage: <command> <file1>'
!            write(6,*)'<file1>: parameter file - where data for simulations are given'
!            pause;
!            ! stop
!        endif
!        if(n1==1)fparam=buf	 !SAND
!		if(n1==2)fparam2=buf !clay
!        n1=n1+1
!    enddo
    !----end command line syntax-----

if (iargc() .NE. 2) then
    write(6,*)'error in the command line:'
    write(6,*)'usage: <command> <param1> <param2>'
    write(6,*)'<param1>: sand fraction (%)'
    write(6,*)'<param2>: clay fraction (%)'
end if
n1=1
call getarg(n1, buf)
fparam=buf
n1=2
call getarg(n1, buf)
fparam2=buf
open(unit=10,file='temp.tmp',status='unknown')
write(10,*) fparam, fparam2
rewind(10)
read(10,*) SAND, clay
close(10,status='delete')

soil_texture=what_texture(SAND,clay)

open(11,file='texture.txt',status='unknown')
write(11,'(a)') trim(soil_texture)
write(6,'(a)')trim(soil_texture)
close(11)

end program	make_texture