PROFILE := default
REGION := ap-northeast-1

APP := efs-mode-change

S3_BUCKET := ${PROFILE}-${APP}-template
STACK_NAME := ${PROFILE}-${APP}-stack

# CloudFormation のテンプレートに渡すパラメータ
MIBPS := "1"

bucket:
	aws s3 mb s3://${S3_BUCKET} \
		--profile ${PROFILE} \
		--region ${REGION}

build:
	sam build

test: build
	sam local invoke \
		--event event.json \
		--template template_test.yaml \
		--parameter-overrides 'ParameterKey=Mibps,ParameterValue=${MIBPS}'

package: build
	sam package \
		--s3-bucket ${S3_BUCKET} \
		--output-template-file packaged.yaml \
		--profile ${PROFILE} \
		--region ${REGION}

deploy: package
	sam deploy \
		--template-file packaged.yaml \
		--stack-name ${STACK_NAME} \
		--capabilities CAPABILITY_IAM \
		--parameter-overrides 'ParameterKey=Mibps,ParameterValue=${MIBPS}' \
		--profile ${PROFILE} \
		--region ${REGION}

clean:
	aws cloudformation delete-stack \
		--stack-name ${STACK_NAME} \
		--profile ${PROFILE} \
		--region ${REGION}
