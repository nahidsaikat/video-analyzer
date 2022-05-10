output "sqs_url" {
  value = aws_sqs_queue.video_queue.id
}
