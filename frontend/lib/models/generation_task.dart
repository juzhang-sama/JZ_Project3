/// 生成任务模型
class GenerationTask {
  final int id;
  final int userId;
  final String prompt;
  final String modelName;
  final String status;
  final int? resultId;
  final String? errorMessage;
  final DateTime createdAt;
  final DateTime? completedAt;

  GenerationTask({
    required this.id,
    required this.userId,
    required this.prompt,
    required this.modelName,
    required this.status,
    this.resultId,
    this.errorMessage,
    required this.createdAt,
    this.completedAt,
  });

  factory GenerationTask.fromJson(Map<String, dynamic> json) {
    return GenerationTask(
      id: json['id'] as int,
      userId: json['user_id'] as int,
      prompt: json['prompt'] as String,
      modelName: json['model_name'] as String,
      status: json['status'] as String,
      resultId: json['result_id'] as int?,
      errorMessage: json['error_message'] as String?,
      createdAt: DateTime.parse(json['created_at'] as String),
      completedAt: json['completed_at'] != null
          ? DateTime.parse(json['completed_at'] as String)
          : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'user_id': userId,
      'prompt': prompt,
      'model_name': modelName,
      'status': status,
      'result_id': resultId,
      'error_message': errorMessage,
      'created_at': createdAt.toIso8601String(),
      'completed_at': completedAt?.toIso8601String(),
    };
  }

  bool get isPending => status == 'pending';
  bool get isProcessing => status == 'processing';
  bool get isCompleted => status == 'completed';
  bool get isFailed => status == 'failed';
}

