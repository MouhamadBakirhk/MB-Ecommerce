<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\ChatMessage;

class ChatMessageController extends Controller
{
     
    public function store(Request $request)
    {
        $data = $request->validate([
            'question' => 'required|string',
            'answer' => 'required|string',
        ]);

        $message = ChatMessage::create($data);

        return response()->json($message, 201);
    }

    
    public function index()
    {
        return response()->json(ChatMessage::latest()->get());
    }
}
