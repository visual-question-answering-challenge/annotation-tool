var add_another_question = function () {

    var question = `<div class="row gray lighten-4">
                        <div class="input-field col s12">
                            <div class="row">
                                <div class="col s10">
                                    <input placeholder="Write a question here" type="text" class="validate dataInput">
                                </div>

                                <div class="col s2">    
                                    <a  class="btn-floating btn waves-effect waves-light red btnRemoveQuestion"><i class="material-icons">clear</i></a>
                                </div>
                            </div>
                        </div>

                    </div>`;

    $("#questions_box").append(question)
}

var remove_question = function () {
    var div = $(this).parent().parent().parent().parent();

    $(div).animate({
        opacity: 0.25,
        left: "+=50",
        height: "toggle"
    }, 250, function () {
        $(div).remove()
    });
}

var get_next_image = function () {

    // getting validation token
    var token = $("[name=csrfmiddlewaretoken]").val();

    // getting each question inserted
    var questionList = [];
    var hasEmptyQuestion = false;
    $(".dataInput").each(function () {
        console.log("QUESTION: " + $(this).val().length);
        // if any question field is empty a erro msg is displayed
        if ($(this).val().length === 0) {
           hasEmptyQuestion = true; 
        } else {
            questionList.push($(this).val());
        }
    });

    if(hasEmptyQuestion){
        $("#modal2").modal('open');
        return;
    }
    

    questionList = questionList.join(";");
    var imagePath = $(".responsive-img").attr('src');
    $.ajax({
        type: 'POST',
        headers: {
            'X-CSRFToken': token
        },
        data: {
            'questionList': questionList,
            'imgPath': imagePath
        },
        url: '/annotation/store_query/',
        success: function (resp) {
            $("#form_content").empty();
            $("#form_content").html(resp);
            $("#btnAddQuestion").on("click", add_another_question);
            $("#questions_box").on("click", ".btnRemoveQuestion", remove_question);
            $("#nextImage").on("click", get_next_image);
            $(".dataInput").focus();
        },
        error: function (a) {
            console.log(a)
        }
    });
}


$(document).keypress(function(e) {
    if(e.which == 13) {
        get_next_image();
    }
});


$(document).ready(function () {

    $('.modal').modal();

    $("#btnAddQuestion").on("click", add_another_question);
    $("#questions_box").on("click", ".btnRemoveQuestion", remove_question);
    $("#nextImage").on("click", get_next_image);

    $(".dataInput").focus();
});