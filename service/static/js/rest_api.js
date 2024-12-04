$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#customer_id").val(res.id);
        $("#customer_name").val(res.name);
        $("#customer_email").val(res.email);
        $("#customer_phone_number").val(res.phone_number);
        $("#customer_address").val(res.address);
        if (res.state == true) {
            $("#customer_state").val("true");
        } else {
            $("#customer_state").val("false");
        }
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#customer_name").val("");
        $("#customer_email").val("");
        $("#customer_phone_number").val("");
        $("#customer_address").val("");
        $("#customer_state").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a Customer
    // ****************************************

    $("#create-btn").click(function () {

        let name = $("#customer_name").val();
        let email = $("#customer_email").val();
        let phone_number = $("#customer_phone_number").val();
        let address = $("#customer_address").val();
        let state = $("#customer_state").val() == "true";

        let data = {
            "name": name,
            "email": email,
            "phone_number": phone_number,
            "address": address,
            "state": state
        };

        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "POST",
            url: "/api/customers",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update a Customer
    // ****************************************

    $("#update-btn").click(function () {

        let customer_id = $("#customer_id").val();
        let name = $("#customer_name").val();
        let email = $("#customer_email").val();
        let phone_number = $("#customer_phone_number").val();
        let address = $("#customer_address").val();
        let state = $("#customer_state").val() == "true";

        let data = {
            "name": name,
            "email": email,
            "phone_number": phone_number,
            "address": address,
            "state": state
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
                type: "PUT",
                url: `/api/customers/${customer_id}`,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a Customer
    // ****************************************

    $("#retrieve-btn").click(function () {

        let customer_id = $("#customer_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/api/customers/${customer_id}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a Customer
    // ****************************************

    $("#delete-btn").click(function () {

        let customer_id = $("#customer_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `/api/customers/${customer_id}`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Customer has been Deleted!")
        });

        ajax.fail(function(res){
            if (res.status === 404) {
                flash_message("Customer not found!");
            }
            else if (res.status === 500) {
                flash_message("Internal Server Error!");
            }
            else {
                flash_message("An unexpected error occurred!");
            }
        });
    });

    $("#suspend-btn").click(function () {

        let customer_id = $("#customer_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "PUT",
            url: `/api/customers/${customer_id}/suspend`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message("http status:"+res.status)
        });

    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#customer_id").val("");
        $("#flash_message").empty();
        clear_form_data()
    });

    // ****************************************
    // Search for a Customer
    // ****************************************

    $("#search-btn").click(function () {

        let name = $("#customer_name").val();
        let email = $("#customer_email").val();
        let phone_number = $("#customer_phone_number").val();
        let address = $("#customer_address").val();
        let state = $("#customer_state").val() == "true";

        let queryString = ""

        if (name) {
            queryString += 'name=' + name
        }
        if (email) {
            if (queryString.length > 0) {
                queryString += '&email=' + email
            } else {
                queryString += 'email=' + email
            }
        }
        if (phone_number) {
            if (queryString.length > 0) {
                queryString += '&phone_number=' + phone_number
            } else {
                queryString += 'phone_number=' + phone_number
            }
        }
        if (address) {
            if (queryString.length > 0) {
                queryString += '&address=' + address
            } else {
                queryString += 'address=' + address
            }
        }
        if (state) {
            if (queryString.length > 0) {
                queryString += '&state=' + state
            } else {
                queryString += 'state=' + state
            }
        }
        

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/api/customers?${queryString}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-2">ID</th>'
            table += '<th class="col-md-2">Name</th>'
            table += '<th class="col-md-2">Email</th>'
            table += '<th class="col-md-2">Phone Number</th>'
            table += '<th class="col-md-2">Address</th>'
            table += '<th class="col-md-2">State</th>'
            table += '</tr></thead><tbody>'
            let firstCustomer = "";
            for(let i = 0; i < res.length; i++) {
                let customer = res[i];
                table +=  `<tr id="row_${i}"><td>${customer.id}</td><td>${customer.name}</td><td>${customer.email}</td><td>${customer.phone_number}</td><td>${customer.address}</td><td>${customer.state}</td></tr>`;
                if (i == 0) {
                    firstCustomer = customer;
                }
            }
            table += '</tbody></table>';
            $("#search_results").append(table);

            // copy the first result to the form
            if (firstCustomer != "") {
                update_form_data(firstCustomer)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

})
