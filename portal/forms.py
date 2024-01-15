from django import forms


class CreateTestForm(forms.Form):
    test_name = forms.CharField(widget=forms.TextInput
                                (attrs={'class': 'form-control',
                                        'placeholder': 'e.g. DSA Example Test',
                                        'id': 'modal-email'}), label='Test Name: ', max_length=50, )

    instruction = forms.CharField(widget=forms.Textarea
                                  (attrs={'class': 'form-control',
                                          'placeholder': 'e.g. Length of thje test is one hour',
                                          'id': 'modal-email'}), label='Test Name: ', max_length=50, required=False)


class EditTestForm(forms.Form):
    test_name = forms.CharField(widget=forms.TextInput
                                (attrs={'class': 'border-b-2 mb-4 text-[17px] hover:border-slate-500 focus:border-orange-400 outline-none text-slate-500',
                                        'placeholder': 'e.g. DSA Example Test',
                                        'id': 'modal-email'}), label='Test Name: ', max_length=50,)

    instruction = forms.CharField(widget=forms.Textarea
                                  (attrs={'class': 'border-2 rounded-md focus:outline-orange-400 mb-4 text-[17px] p-4 outline-1 hover:border-slate-500 text-slate-500',
                                          'placeholder': 'e.g. Length of the test is one hour',
                                          'id': 'modal-email'}), label='Test Name: ', max_length=50, required=False)


class AddQuestionForm(forms.Form):
    question = forms.CharField(widget=forms.Textarea
                               (attrs={'class': 'form-control',
                                       'placeholder': 'Enter the Question',
                                       'id': 'floatingTextarea'}), label='Test Name: ', required=True)
    questionIsCode = forms.BooleanField(required=False)

    op1 = forms.CharField(widget=forms.Textarea
                          (attrs={'class': 'form-control',
                                  'placeholder': 'Enter Option 1',
                                  'id': 'floatingTextarea'}), label='Test Name: ', required=True)
    op1IsCode = forms.BooleanField(required=False)

    op2 = forms.CharField(widget=forms.Textarea
                          (attrs={'class': 'form-control',
                                  'placeholder': 'Enter Option 2',
                                  'id': 'floatingTextarea'}), label='Test Name: ', required=True)
    op2IsCode = forms.BooleanField(required=False)

    op3 = forms.CharField(widget=forms.Textarea
                          (attrs={'class': 'form-control',
                                  'placeholder': 'Enter Option 3',
                                  'id': 'floatingTextarea'}), label='Test Name: ', required=True)
    op3IsCode = forms.BooleanField(required=False)

    op4 = forms.CharField(widget=forms.Textarea
                          (attrs={'class': 'form-control',
                                  'placeholder': 'Enter Option 4',
                                  'id': 'floatingTextarea'}), label='Test Name: ', required=True)
    op4IsCode = forms.BooleanField(required=False)

    correct_op = forms.CharField(label='Correct Option', widget=forms.TextInput(
        attrs={'min': 1, 'max': '4', 'type': 'number', 'class': 'form-control', 'id': 'floatingInput'}))
