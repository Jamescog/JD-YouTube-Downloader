$(document).ready(() => {
    // function showProcessingCircle() {
    //         $(".processing-circle").show();
    //     }

    // // Function to hide the processing circle
    // function hideProcessingCircle() {
    //     $(".processing-circle").hide();
    // }
    $("#goButton").click(() => {
        const Uurl = $("#youtubeUrlInput").val();
        if (Uurl === "") {
            $(".warn-text").removeClass("d-none");
            return;
        }
        $(".warn-text").addClass("d-none");

        $("#circle").removeClass("d-none").addClass("processing-circle");

        $.ajax({
            url: "http://localhost:5000/meta-data" + `?url=${Uurl}`,
            type: "GET",
            success: (data) => {
                const files = data.videos;
                $("#circle").removeClass("processing-circle").addClass("d-none");
                $("#data-table").removeClass("d-none");
                var videoDataBody = $('#videoDataBody');
                videoDataBody.empty(); // Clear the table before adding new rows
                $.each(files, function (key, value) {
                    var row = $('<tr>');

                    var resolutionColumn = $('<td>').text(value.resolution);
                    row.append(resolutionColumn);

                    var fileSizeColumn = $('<td>').text(value.file_size);
                    row.append(fileSizeColumn);

                    var subtypeColumn = $('<td>').text(value.subtype);
                    row.append(subtypeColumn);

                    var downloadColumn = $('<td>');
                    var downloadLink = $('<a>').attr('href', '#').attr('data-key', key);
                    var downloadIcon = $('<i>').addClass('fas fa-download');
                    downloadLink.append(downloadIcon);
                    downloadColumn.append(downloadLink);
                    row.append(downloadColumn);

                    videoDataBody.append(row);
                });
                $("#title").text(data.title);
                $("#duration").text(data.duration);
                $("#info-div").removeClass("d-none");
                $("#data-table").removeClass("d-none");
                videoDataBody.on('click', 'a', function () {
                    var key = $(this).data('key');
                    $.ajax({
                        url: `http://localhost:5000/download?url=${Uurl}&itag=${key}`,
                        success: (data) => {
                            //create a tag with href as the data uri and _blank to open in new tab
                            var a = $("<a>").attr("href", data).attr("target", "_blank");
                            //just click the element to download
                            a[0].click();
                        }
                });
                    });

            },
            error: (err) => {
                console.log(err);
            }
        });
    });
});
