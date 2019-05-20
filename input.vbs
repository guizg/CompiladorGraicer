function fibonacci(n as integer) as integer
    dim flag as boolean
    flag = false
    if n = 0 then
        fibonacci = 1
        flag = true
    end if

    if n = 1 then 
        fibonacci = 1
        flag = true
    end if

    if flag = false then
        fibonacci = fibonacci(n-2) + fibonacci(n-1)
    end if

end function

sub countdown(n as integer)
    if n>0 then
        print n
        call countdown(n-1)
    end if
end sub

sub main()
    ' call countdown(5)
    print fibonacci(5)
end sub

