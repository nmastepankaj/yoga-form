from main.models import Account, Admission, Payment

class AdmissionService:

    def register(self, data) -> [bool, str]:
        first_name = data['first_name']
        last_name= data['last_name']
        age = data['age']
        email = data['email']
        mobile_number = data['mobile_number']
        gender= data['gender']
        batch_id = data['batch_id']
        amount = data['amount']
        payment= data['payment_successful']

        if Account.objects.filter(email=email).exists():
            account = Account.objects.filter(email=email).first()
        else:
            account = Account.objects.create(first_name=first_name,last_name=last_name,age=age,email=email,mobile_number=mobile_number,gender=gender, batch_id=batch_id)
        
        payment_object = Payment.objects.create(user=account,amount=amount,payment_successful=payment)
        payment_object.payment_id = payment_object.getnerate_payment_id()
        payment_object.save()
        # url_test = 'https://web-production-7af1.up.railway.app/completePayment'
        # send_mail('Yoga For Life - Payment Link',
        # 'Dear '+f_name+',\n\nThanks for enrolling in our yoga class.\nCharges: Rs 500/month\nKindly make the payment with the link given below. You can make the payment within 30 days of enrolment to confirm your admission.\n\nLink:'+url_test+'\n\nThank you and see you soon:)\n\nBest,\nSanya',
        # 'zaverisanya@gmail.com',[e],fail_silently=True)
        if payment:
            admission = Admission.objects.create(payment=payment_object,user=account,batch_id=batch_id)
            admission.admission_id = admission.generate_admission_id()
            admission.save()

            return True, "Registered Successfully"
        
        return False, "Payment Not Verified"
    
    def update_form(self, data):
        email = data['email']
        batch_id = data['batch_id']
        amount = data['amount']
        payment= data['payment_successful']

        account = Account.objects.filter(email=email).first()
        account.batch_id = batch_id
        account.save()
        
        payment_object = Payment.objects.create(user=account,amount=amount,payment_successful=payment)
        payment_object.payment_id = payment_object.getnerate_payment_id()
        payment_object.save()
       
        if payment:
            admission = Admission.objects.create(payment=payment_object,user=account,batch_id=batch_id)
            admission.admission_id = admission.generate_admission_id()
            admission.save()

            return True, "Updated Successfully"
        
        return False, "Payment Not Verified"


        