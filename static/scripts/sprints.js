class addSprintDialog
{
    constructor()
    {
        this.dialog = document.getElementById('_add_dialog');
        this.openBtn = document.getElementById('_add_sprint');
        this.closeBtn = document.getElementById('_dialog_close');
        this.openBtnBig = document.getElementById('_add_sprint_big');

        if (this.openBtnBig !== null) {this.openBtnBig.addEventListener('click', this.#open);}
        this.openBtn.addEventListener('click', this.#open);
        this.closeBtn.addEventListener('click', this.#close);

    }

    #open = e => {
        this.dialog.showModal();
    }

    #close = e => {
        this.dialog.close();
    }
}


function renderSprints()
{
    function getdaysBetweenDates(date_start, date_end)
    {
        const diffTime = Math.abs(date_end - date_start);
        return Math.floor(diffTime / (1000 * 60 * 60 * 24)); 
    }

    const sprints = document.querySelectorAll('div.sprint');
    sprints.forEach(sprint => {

        const date_start_element = sprint.querySelector('div.start-date');
        const date_due_element = sprint.querySelector('div.due-date');
        const day_txt_start = sprint.querySelector('div.start-days');
        const day_txt_due = sprint.querySelector('div.due-days');

        const date_start = new Date(date_start_element.dataset.date);
        const date_due = new Date(date_due_element.dataset.date);
        const date_now = new Date();

        const diff_start = getdaysBetweenDates(date_start, date_now);
        const diff_due = getdaysBetweenDates(date_now, date_due);

        const sprint_has_started = (date_start.getTime() < date_now.getTime());
        const sprint_has_ended = (date_due.getTime() < date_now.getTime());

        day_txt_start.innerText = sprint_has_started ? "Started " + diff_start + " days ago" : "Starts in " + diff_start + " days";
        day_txt_due.innerText = sprint_has_ended ? "Ended " + diff_due + " days ago" :  "Ends in " + diff_due + " days";

        let style_day_txt_start = 'normal';
        let style_day_txt_due = 'normal';
        if (sprint_has_started)
        {
            if (sprint_has_ended)
            {
                style_day_txt_due = "warning";
            }
            else
            {
                if (diff_due <= 3) {style_day_txt_due = "warning";}
                else if (diff_due <= 7) {style_day_txt_due = "caution";}
            }
        }
        else
        {
            if (diff_start <= 3) {style_day_txt_start = "warning";}
            else if (diff_start <= 7) {style_day_txt_start = "caution";}
        }

        day_txt_start.classList.add(style_day_txt_start);
        day_txt_due.classList.add(style_day_txt_due);
    });
}

function renderChart(chart_data, idSuffix = '')
{
    const ctx = document.getElementById('myChart' + idSuffix);

    if (ctx == undefined) {return false;}

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['TODO', 'WIP', 'DONE'],
            datasets: [{
                label: 'Tasks',
                data: [chart_data.todo, chart_data.wip, chart_data.done],
                backgroundColor: [
                    '#af0000', // Red slice
                    'orange', // Blue slice
                    'green'
                ],
                borderWidth: 1
            }]
        },
        options: {
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false,
                },
                tooltip: {
                    enabled: false,
                }
            }
        }
    });

    const total_el = document.getElementById('_chart_total' + idSuffix);
    total_el.innerText = chart_data.todo + chart_data.wip + chart_data.done;

    const todo_legend = document.getElementById('_chart_legend_todo' + idSuffix);
    const wip_legend = document.getElementById('_chart_legend_wip' + idSuffix);
    const done_legend = document.getElementById('_chart_legend_done' + idSuffix);

    todo_legend.innerText = chart_data.todo + " tasks todo";
    wip_legend.innerText = chart_data.wip + " tasks in progress";
    done_legend.innerText = chart_data.done + " tasks completed";
}

new addSprintDialog();
renderSprints();
renderChart(chart_data);
renderChart(current_chart_data, '_current');