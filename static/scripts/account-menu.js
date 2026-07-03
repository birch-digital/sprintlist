class AccountMenu
{
    constructor()
    {
        this.menu = document.querySelector('.account-menu');
        if (this.menu === null) {return;}

        document.addEventListener('click', this.#handleClick);
    }

    #handleClick = e => {
        if (!this.menu.open) {return;}
        if (!this.menu.contains(e.target)) {
            this.menu.open = false;
        }
    }
}

new AccountMenu();
