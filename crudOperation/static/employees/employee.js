$(document).ready(function () {

    let editMode = false;
    let employeeUuid = null;
    $('#message-status').hide();


    // -----------------------------------------
    // CSRF
    // -----------------------------------------

    function getCookie(name) {

        let cookieValue = null;

        if (document.cookie && document.cookie !== '') {

            const cookies = document.cookie.split(';');

            for (let cookie of cookies) {

                cookie = cookie.trim();

                if (cookie.substring(0, name.length + 1) === (name + '=')) {

                    cookieValue =
                        decodeURIComponent(
                            cookie.substring(
                                name.length + 1
                            )
                        );
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!this.crossDomain) {
                xhr.setRequestHeader(
                    "X-CSRFToken",
                    csrftoken
                );
            }
        }
    });


    // -----------------------------------------
    // Clear Form
    // -----------------------------------------

    function clearForm() {
        $('#employeeForm')[0].reset();
        $('#employeeUuid').val('');
        $('.form-control').removeClass('is-invalid');
        $('.invalid-feedback').html('');
    }


    // -----------------------------------------
    // Add Employee
    // -----------------------------------------

    $('#btnAddEmployee').click(function () {

        editMode = false;
        employeeUuid = null;

        clearForm();

        $('#modalTitle').text('Add Employee');
        $('#btnSaveEmployee').text('Add Employee');
        $('#employeeModal').modal('show');
    });


    // -----------------------------------------
    // Save / Update
    // -----------------------------------------

    $('#employeeForm').submit(function (e) {

        e.preventDefault();
        $('.form-control').removeClass('is-invalid');
        $('.invalid-feedback').html('');

        let url;

        if (editMode) {
            url = `/employees/${employeeUuid}/update/`;
        } else {
            url = CREATE_URL;
        }

        $('#btnSaveEmployee').prop('disabled', true);

        $.ajax({
            url: url,
            type: 'POST',
            data: $(this).serialize(),
            success: function (response) {
                if (response.success) {
                    $('#employeeModal').modal('hide');
                    $('#message-status').text(response.message).show();
                    console.log(response.message);
                    location.reload();
                }
            },
            error: function (xhr) {
                $('#btnSaveEmployee').prop('disabled', false);

                if (xhr.responseJSON && xhr.responseJSON.errors) {
                    showErrors(
                        xhr.responseJSON.errors
                    );
                } else {
                    alert('Something went wrong.');
                }
            },
            complete: function () {
                $('#btnSaveEmployee').prop('disabled', false);
            }
        });
    });

    // -----------------------------------------
    // Display Validation Errors
    // -----------------------------------------

    function showErrors(errors) {

        $.each(
            errors,
            function (field, messages) {

                let errorMessage = '';

                messages.forEach(function (message) {
                    errorMessage += message.message + '<br>';
                });

                $('#' + field).addClass('is-invalid');
                $('#error_' + field).html(errorMessage);
            }
        );
    }


    // -----------------------------------------
    // Edit Employee
    // -----------------------------------------

    $(document).on('click', '.btnEdit', function () {

            employeeUuid = $(this).data('uuid');
            editMode = true;
            clearForm();

            $.ajax({
                url: `/employees/${employeeUuid}/`,
                type: 'GET',
                success: function (response) {
                    if (response.success) {
                        const employee = response.employee;
                        $('#emp_name').val(employee.name);
                        $('#emp_email').val(employee.email);
                        $('#emp_address').val(employee.address);
                        $('#emp_phone').val(employee.phone);
                        $('#employeeUuid').val(employee.uuid);
                        $('#modalTitle').text('Edit Employee');
                        $('#btnSaveEmployee').text('Update Employee');
                        $('#employeeModal').modal('show');
                    }
                },
                error: function () {
                    alert('Unable to load employee.');
                }
            });
        }
    );


    // -----------------------------------------
    // Delete Employee
    // -----------------------------------------

    $(document).on('click', '.btnDelete', function () {
            const uuid = $(this).data('uuid');
            if (!confirm('Are you sure you want to delete this employee?')) {
                return;
            }
            $.ajax({
                url:`/employees/${uuid}/delete/`,
                type: 'POST',
                success: function (response) {
                    if (response.success) {
                        $('#employee-' + uuid).fadeOut(
                            300,
                            function () {
                                $(this).remove();
                            }
                        );
                    }
                },
                error: function () {
                    alert('Unable to delete employee.');
                }
            });
        }
    );


    // -----------------------------------------
    // Search
    // -----------------------------------------

    let searchTimer;

    $('#searchEmployee').on('keyup', function () {

            clearTimeout(searchTimer);
            const search = $(this).val();
            searchTimer = setTimeout(function () {
                window.location.href = `?search=${encodeURIComponent(search)}`;
            }, 500);
        }
    );
    
});