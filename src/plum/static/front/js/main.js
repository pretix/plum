$(function () {
    $('[data-toggle="tooltip"]').tooltip();
    $("[data-formset]").formset(
        {
            animateForms: true,
            reorderMode: 'animate'
        }
    );
});