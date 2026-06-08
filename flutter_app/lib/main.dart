import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

void main() {
  runApp(const LlamaApp());
}

class LlamaApp extends StatelessWidget {
  const LlamaApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Local LLM Client',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorSchemeSeed: Colors.blue,
        useMaterial3: true,
      ),
      home: const LlamaHomePage(),
    );
  }
}

class LlamaHomePage extends StatefulWidget {
  const LlamaHomePage({super.key});

  @override
  State<LlamaHomePage> createState() => _LlamaHomePageState();
}

class _LlamaHomePageState extends State<LlamaHomePage> {
  final TextEditingController serverController = TextEditingController(
    text: 'http://192.168.100.39:5000',
  );
  final TextEditingController questionController = TextEditingController();
  final TextEditingController answerController = TextEditingController();

  bool isLoading = false;

  Future<void> askLlama() async {
    final serverBaseUrl = serverController.text.trim();
    final question = questionController.text.trim();

    if (serverBaseUrl.isEmpty) {
      answerController.text = 'Please enter the Flask server URL first.';
      return;
    }

    if (question.isEmpty) {
      answerController.text = 'Please enter a question first.';
      return;
    }

    setState(() {
      isLoading = true;
      answerController.text = 'Waiting for local LLM response...';
    });

    try {
      final encodedQuestion = Uri.encodeComponent(question);

      // Important: format=json is required because the mobile app expects JSON.
      final url = Uri.parse('$serverBaseUrl/ask?q=$encodedQuestion&format=json');

      final response = await http.get(url).timeout(
            const Duration(seconds: 180),
          );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        if (data is Map && data.containsKey('answer')) {
          answerController.text = data['answer'].toString();
        } else {
          answerController.text = response.body;
        }
      } else {
        answerController.text =
            'Server error: ${response.statusCode}\n${response.body}';
      }
    } catch (e) {
      answerController.text = 'Connection error.\n\nMake sure:\n'
          '1. Your phone and laptop are on the same Wi-Fi.\n'
          '2. Flask is running on port 5000.\n'
          '3. llama-server is running on port 8080.\n'
          '4. The server IP is correct.\n'
          '5. Android cleartext HTTP is allowed.\n\n'
          'Error details:\n$e';
    } finally {
      setState(() {
        isLoading = false;
      });
    }
  }

  void clearFields() {
    questionController.clear();
    answerController.clear();
  }

  @override
  void dispose() {
    serverController.dispose();
    questionController.dispose();
    answerController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Local LLM Client'),
        centerTitle: true,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            TextField(
              controller: serverController,
              decoration: const InputDecoration(
                labelText: 'Flask Server URL',
                hintText: 'Example: http://192.168.100.39:5000',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 12),
            TextField(
              controller: questionController,
              minLines: 2,
              maxLines: 4,
              decoration: const InputDecoration(
                labelText: 'Question',
                hintText: 'Example: What is cloud computing?',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 12),
            Row(
              children: [
                Expanded(
                  child: ElevatedButton(
                    onPressed: isLoading ? null : askLlama,
                    child: isLoading
                        ? const Text('Waiting...')
                        : const Text('Send to Local LLM'),
                  ),
                ),
                const SizedBox(width: 8),
                ElevatedButton(
                  onPressed: isLoading ? null : clearFields,
                  child: const Text('Clear'),
                ),
              ],
            ),
            const SizedBox(height: 12),
            Expanded(
              child: TextField(
                controller: answerController,
                readOnly: true,
                expands: true,
                maxLines: null,
                minLines: null,
                textAlignVertical: TextAlignVertical.top,
                decoration: const InputDecoration(
                  labelText: 'LLaMA Reply',
                  border: OutlineInputBorder(),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
