program e02_mmc

    use mmc
    implicit none 
    integer, parameter :: dp = selected_real_kind(15, 307)
    real(kind=dp) :: Vol, Var
    real :: p(0:5), t_start, t_end
    integer :: j,   i, inside, N, Nl(1:4), S

    print *, "E02 > Volumenes en R6 / MMC 2025 (FORTRAN 2008)"
    print *, "(c) Carlos M. Martinez"

    Nl = (/10**6, 10**7, 10**8, 10**9/)

    call random_seed()

    do j = 1,size(Nl)
        call cpu_time(t_start)
        N = Nl(j)
        S = 0
        Var = 0
        Vol = 0    
        do i = 0, N
            p = RandR6Point() 
            inside = IsInsideVolume(p)
            if ( inside == 1) then
                S = S + 1
            end if
            ! print *, '(',p,') => ', inside
        end do
        
        Vol = real(S) / real(N)
        Var = (real(S) / N )*(1-real(S)/N)/(N-1)
    
        call cpu_time(t_end)
        print *, ": N=",N ," Vol:", Vol, " | Var: ", Var, " | time: ", (t_end-t_start)     
    end do 

end program e02_mmc

!--------------------------------------------------------

module mmc
    implicit none

contains

    real function returnnumber()
        implicit none
        real :: n
        n = 83.4
        returnnumber = n
    end function returnnumber

    ! This functions generates a random, uniformly distributed, point in R6
    function RandR6Point() result(Point)
        implicit none
        real :: Point(0:5)

        ! Point = (/1.0, 2.0, 3.0 , 4.0 , 5.0 ,6.0/)
        call random_number(Point)
        
    end function RandR6Point

    ! Esta funcion devuelve 0 o 1 segun el punto pasado como parametro este
    ! o no dentro del volumen de la hiperesfera en R6
    function IsInsideVolume(Point) result(isInside)
        implicit none
        integer :: isInside
        real :: Point(0:5), d

        ! calculate distance from center
        d = sqrt( & 
            (Point(0)-0.45)**2 + &
            (Point(1)-0.50)**2 + &
            (Point(2)-0.60)**2 + &
            (Point(3)-0.60)**2 + &
            (Point(4)-0.50)**2 + &
            (Point(5)-0.45)**2   &     
        )

        ! if distance is less than the hypersphere's radius, then the point 
        ! is inside the volume
        if (d < 0.35 ) then
            isInside = 1
        else 
            isInside = 0
        end if
        
    end function IsInsideVolume

end module mmc 