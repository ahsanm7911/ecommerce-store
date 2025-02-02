var script = document.createElement('script')
script.type = 'text/javascript'
script.src = "https://cdn.tiny.cloud/1/296ivbk1ihcf2wqxhqucf5wojihhnmfl1m2izja11b2mj36y/tinymce/6/tinymce.min.js"

document.head.appendChild(script)

script.onload = function(){

    tinymce.init({
        selector: '#id_description',
    plugins: 'anchor autolink charmap codesample emoticons image link lists media searchreplace table visualblocks wordcount checklist mediaembed casechange export formatpainter pageembed linkchecker a11ychecker tinymcespellchecker permanentpen powerpaste advtable advcode editimage tinycomments tableofcontents footnotes mergetags autocorrect typography inlinecss',
    toolbar: 'undo redo | blocks fontfamily fontsize | bold italic underline strikethrough | link image media table mergetags | addcomment showcomments | spellcheckdialog a11ycheck typography | align lineheight | checklist numlist bullist indent outdent | emoticons charmap | removeformat',
    tinycomments_mode: 'embedded',
    tinycomments_author: 'Author name',
    mergetags_list: [
        { value: 'First.Name', title: 'First Name' },
      { value: 'Email', title: 'Email' },
    ]
  });
}