from django.shortcuts import redirect

def  Login_Redirect(request):
	return redirect('/app/login')