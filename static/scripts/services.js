function taskRowId(row)
{
    const idInput = row.querySelector('input[name$="-id"]');
    return idInput ? idInput.value : '';
}

function bindTaskRow(row, container)
{
    const titleInput = row.querySelector('input[type="text"]');
    const removeBtn = row.querySelector('.remove-task-row');

    titleInput.addEventListener('input', () => {
        if (row.classList.contains('is-empty') && titleInput.value.trim() !== '')
        {
            row.classList.remove('is-empty');
            addTaskRow(container);
        }
    });

    removeBtn.addEventListener('click', () => {
        if (taskRowId(row) !== '')
        {
            const deleteInput = row.querySelector('input[name$="-DELETE"]');
            deleteInput.checked = true;
            row.style.display = 'none';
        }
        else
        {
            row.remove();
        }
    });
}

function addTaskRow(container)
{
    const prefix = container.dataset.prefix;
    const totalFormsInput = document.getElementById('id_' + prefix + '-TOTAL_FORMS');
    const nextIndex = parseInt(totalFormsInput.value, 10);

    const template = container.parentElement.querySelector(
        'template.task-row-template[data-prefix="' + prefix + '"]'
    );
    const html = template.innerHTML.replaceAll('__prefix__', nextIndex);

    const wrapper = document.createElement('div');
    wrapper.innerHTML = html.trim();
    const newRow = wrapper.firstElementChild;

    container.appendChild(newRow);
    totalFormsInput.value = nextIndex + 1;

    bindTaskRow(newRow, container);
}

function initTaskChecklist(container)
{
    container.querySelectorAll('.task-template-row').forEach(row => bindTaskRow(row, container));
}

function bindStepper(stepper)
{
    const input = stepper.querySelector('input[type="number"]');
    const decBtn = stepper.querySelector('.stepper-decrement');
    const incBtn = stepper.querySelector('.stepper-increment');

    decBtn.addEventListener('click', () => {
        const current = parseInt(input.value, 10) || 0;
        input.value = Math.max(0, current - 1);
    });

    incBtn.addEventListener('click', () => {
        const current = parseInt(input.value, 10) || 0;
        input.value = current + 1;
    });
}

function initDialogs()
{
    document.querySelectorAll('dialog').forEach(dialog => {
        dialog.querySelectorAll('[data-dialog-close]').forEach(btn => {
            btn.addEventListener('click', () => dialog.close());
        });
    });

    document.querySelectorAll('[data-open-dialog]').forEach(trigger => {
        trigger.addEventListener('click', () => {
            const dialog = document.getElementById(trigger.dataset.openDialog);
            if (dialog) {dialog.showModal();}
        });
    });
}

document.querySelectorAll('.task-template-list').forEach(initTaskChecklist);
document.querySelectorAll('.stepper').forEach(bindStepper);
initDialogs();
