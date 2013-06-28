function do_translate() {
    var newlang = $('#lang').value();
    var paths = [];
    $('.i18n').each(function(elem) {
        paths.push(elem.attr('path'));
    });
    var i18n = API().i18n.get(newlang, paths);
    $('.i18n').each(function(elem) {
        $(elem).text(i18n[elem.attr('path')]);
    });
    return false;
}