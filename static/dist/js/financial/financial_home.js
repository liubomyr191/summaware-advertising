const manageCompanyBtn 		= document.querySelector('#manage_company');
const manageLocationBtn 	= document.querySelector('#manage_location');
const manageDepartmentBtn 	= document.querySelector('#manage_department');
const manageProfitBtn 		= document.querySelector('#manage_profit');
const manageGLBtn 			= document.querySelector('#manage_gl');

const manageCompanyWindow 	 = document.querySelector('#financial_company_code');
const manageLocationWindow 	 = document.querySelector('#financial_location_code');
const manageDepartmentWindow = document.querySelector('#financial_department_code');
const manageProfitWindow 	 = document.querySelector('#financial_profit_code');
const manageGLWindow 		 = document.querySelector('#financial_gl_code');

const buttonInactiveColor = "#9999b6";
const buttonActiveColor = "#21215F";


manageCompanyBtn.addEventListener('click', e => {
    e.preventDefault();

	resetButtonColor();
	hideAllWindow();

	manageCompanyBtn.style.backgroundColor = buttonActiveColor;
	manageCompanyWindow.style.display = "block";

});

manageLocationBtn.addEventListener('click', e => {
    e.preventDefault();

	resetButtonColor();
	hideAllWindow();
	
	manageLocationBtn.style.backgroundColor = buttonActiveColor;
	manageLocationWindow.style.display = "block";
});

manageDepartmentBtn.addEventListener('click', e => {
    e.preventDefault();

	resetButtonColor();
	hideAllWindow();

	manageDepartmentBtn.style.backgroundColor = buttonActiveColor;
	manageDepartmentWindow.style.display = "block";
});

manageProfitBtn.addEventListener('click', e => {
    e.preventDefault();

	resetButtonColor();
	hideAllWindow();

	manageProfitBtn.style.backgroundColor = buttonActiveColor;
	manageProfitWindow.style.display = "block";
});

manageGLBtn.addEventListener('click', e => {
    e.preventDefault();

	resetButtonColor();
	hideAllWindow();

	manageGLBtn.style.backgroundColor = buttonActiveColor;
	manageGLWindow.style.display = "block";
});


function resetButtonColor() {
	manageCompanyBtn.style.backgroundColor = buttonInactiveColor;
	manageLocationBtn.style.backgroundColor = buttonInactiveColor;
	manageDepartmentBtn.style.backgroundColor = buttonInactiveColor;
	manageProfitBtn.style.backgroundColor = buttonInactiveColor;
	manageGLBtn.style.backgroundColor = buttonInactiveColor;
}

function hideAllWindow() {
	manageCompanyWindow.style.display = "none";
	manageLocationWindow.style.display = "none";
	manageDepartmentWindow.style.display = "none";
	manageProfitWindow.style.display = "none";
	manageGLWindow.style.display = "none";
}