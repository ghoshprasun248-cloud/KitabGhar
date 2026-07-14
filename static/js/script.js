/* =====================================================
   KitabGhar Main JavaScript
===================================================== */





document.addEventListener(
    "DOMContentLoaded",
    function()
    {



        /* =====================================================
           Auto Hide Flash Messages
        ===================================================== */


        let alerts = document.querySelectorAll(
            ".alert"
        );


        alerts.forEach(
            function(alert)
            {


                setTimeout(
                    function()
                    {

                        alert.style.display = "none";

                    },

                    5000

                );


            }

        );








        /* =====================================================
           Password Confirmation Validation
        ===================================================== */


        let registerForm = document.querySelector(
            "form[action*='register']"
        );



        if(registerForm)
        {


            registerForm.addEventListener(
                "submit",
                function(event)
                {


                    let password =
                    document.querySelector(
                        "input[name='password']"
                    );


                    let confirmPassword =
                    document.querySelector(
                        "input[name='confirm_password']"
                    );



                    if(
                        password &&
                        confirmPassword &&
                        password.value !== confirmPassword.value
                    )
                    {


                        event.preventDefault();


                        alert(
                            "Passwords do not match!"
                        );


                    }



                }

            );


        }









        /* =====================================================
           Delete Confirmation
        ===================================================== */


        let deleteButtons =
        document.querySelectorAll(
            ".delete-btn"
        );



        deleteButtons.forEach(
            function(button)
            {


                button.addEventListener(
                    "click",
                    function(event)
                    {


                        let confirmDelete =
                        confirm(
                            "Are you sure you want to delete?"
                        );



                        if(!confirmDelete)
                        {

                            event.preventDefault();

                        }


                    }

                );


            }

        );









        /* =====================================================
           Search Animation
        ===================================================== */


        let searchInput =
        document.querySelector(
            "input[name='q']"
        );



        if(searchInput)
        {


            searchInput.addEventListener(
                "keyup",
                function()
                {


                    if(this.value.length > 2)
                    {


                        this.style.borderColor =
                        "#198754";


                    }

                    else
                    {


                        this.style.borderColor =
                        "";


                    }



                }

            );


        }









        /* =====================================================
           Reading Progress
        ===================================================== */


        let reader =
        document.querySelector(
            ".reader-content"
        );



        if(reader)
        {


            window.addEventListener(
                "scroll",
                function()
                {


                    let scrollTop =
                    window.scrollY;



                    let documentHeight =
                    document.documentElement.scrollHeight
                    -
                    window.innerHeight;



                    let progress =
                    (
                        scrollTop /
                        documentHeight
                    )
                    *
                    100;




                    let progressBar =
                    document.querySelector(
                        ".progress-bar"
                    );



                    if(progressBar)
                    {


                        progressBar.style.width =
                        progress + "%";



                        progressBar.innerHTML =
                        Math.round(progress)
                        +
                        "%";


                    }




                }

            );


        }








        /* =====================================================
           Smooth Scrolling
        ===================================================== */


        document.querySelectorAll(
            "a[href^='#']"
        )
        .forEach(
            function(link)
            {


                link.addEventListener(
                    "click",
                    function(event)
                    {


                        let target =
                        document.querySelector(
                            this.getAttribute(
                                "href"
                            )
                        );



                        if(target)
                        {


                            event.preventDefault();


                            target.scrollIntoView(
                                {
                                    behavior:
                                    "smooth"
                                }
                            );


                        }



                    }

                );


            }

        );








    }

);