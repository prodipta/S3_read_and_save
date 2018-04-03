# S3_read_and_save
An Amazon Lambda function to read and extract attachments from mails in S3 and saves to the same bucket

This lambda function is triggered when an S3 object is created. A mail is expected to arrive in `mail/` directory (i.e. keyword is `mail/myemailmessage`). If indeed it does, the lambda function tries to extract all attachments in the mail message and saves them in the output (specified by `output_prefix`) folder. For a similar example see [here](https://docs.aws.amazon.com/lambda/latest/dg/with-s3-example.html).

One of the use case is receiving incoming mails through SES which is routed to an S3 bucket and then the lambda is triggered to extract attachments (which can be data files or reports etc). For the lambda to work, S3 with the specified resource must be added as a trigger (for example in the function designer page) and the lambda function must have correct permission (in particular `Execution Role` action must include `s3:PutObject` and `s3:GetObject`)

Caution: the input and the output directory must be different. Otherwise this may trigger a recursive call of this function.
