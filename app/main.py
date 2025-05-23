from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import json

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/memo")
async def add_memo(request: Request):
    form_data = await request.form()
    new_content = form_data.get("content", "").strip()
    
    if not new_content:
        return templates.TemplateResponse(
            "memo_result.html",
            {"request": request, "message": "请输入内容"}
        )
    
    try:
        with open("data/memo.html", "r", encoding="utf-8") as f:
            existing_content = f.read()
    except FileNotFoundError:
        existing_content = ""
    
    full_content = f"{existing_content}\n{new_content}" if existing_content else new_content
    
    with open("data/memo.html", "w", encoding="utf-8") as f:
        f.write(full_content)
    
    # 注释掉调用API的代码
    # try:
    #     from .llm_agent import LLMAgent
    #     agent = LLMAgent()
    #     tasks = agent.analyze_memo(full_content)
    #     agent.save_todo(tasks)
    # except Exception:
    #     pass

    # 触发备忘录内容更新
    headers = {"HX-Trigger": "memo-updated"}
    return templates.TemplateResponse(
        "memo_result.html",
        {"request": request, "message": "备忘录已保存"},
        headers=headers
    )

@app.delete("/delete-memo/{memo_index}")
async def delete_memo(request: Request, memo_index: int):
    try:
        with open("data/memo.html", "r", encoding="utf-8") as f:
            content = f.read()
        
        lines = [line for line in content.split('\n') if line.strip()]
        
        if 0 <= memo_index < len(lines):
            lines.pop(memo_index)
            
            with open("data/memo.html", "w", encoding="utf-8") as f:
                f.write('\n'.join(lines))
            
            # 移除或注释掉以下代码以避免调用API
            # try:
            #     from .llm_agent import LLMAgent
            #     agent = LLMAgent()
            #     tasks = agent.analyze_memo('\n'.join(lines))
            #     agent.save_todo(tasks)
            # except Exception:
            #     pass
            
            # 返回更新后的备忘录列表
            return templates.TemplateResponse(
                "memo_content.html",
                {"request": request, "content": lines}
            )
            
    except Exception:
        return templates.TemplateResponse(
            "memo_content.html",
            {"request": request, "content": []}
        )

@app.get("/todo")
async def get_todo():
    try:
        with open("data/todo.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"tasks": []}

@app.get("/current-memo")
async def get_current_memo(request: Request):
    try:
        with open("data/memo.html", "r", encoding="utf-8") as f:
            content = f.read()
        return templates.TemplateResponse(
            "memo_content.html", 
            {"request": request, "content": content.split('\n')}
        )
    except FileNotFoundError:
        return templates.TemplateResponse(
            "memo_content.html", 
            {"request": request, "content": ["暂无备忘录内容"]}
        )

@app.get("/todo-list")
async def get_todo_list(request: Request):
    try:
        with open("data/todo.json", "r", encoding="utf-8") as f:
            try:
                tasks = json.load(f)
            except json.JSONDecodeError:
                tasks = {"tasks": []}
        return templates.TemplateResponse(
            "todo_list.html",
            {"request": request, "tasks": tasks.get("tasks", [])}
        )
    except FileNotFoundError:
        # Create empty todo.json file with initial structure
        initial_data = {"tasks": []}
        with open("data/todo.json", "w", encoding="utf-8") as f:
            json.dump(initial_data, f)
        return templates.TemplateResponse(
            "todo_list.html",
            {"request": request, "tasks": []}
        )

@app.get("/load-memo")
async def load_memo():
    try:
        with open("data/memo.html", "r", encoding="utf-8") as f:
            content = f.read()
        return content
    except FileNotFoundError:
        return ""

@app.post("/clear-memo")
async def clear_memo(request: Request):
    try:
        with open("data/memo.html", "w", encoding="utf-8") as f:
            f.write("")
        return templates.TemplateResponse(
            "memo_content.html",
            {"request": request, "content": []}
        )
    except Exception:
        return {"error": "无法删除备忘录内容"}


@app.delete("/delete-task/{task_index}")
async def delete_task(request: Request, task_index: int):
    try:
        with open("data/todo.json", "r", encoding="utf-8") as f:
            tasks = json.load(f)
        
        if 0 <= task_index < len(tasks["tasks"]):
            tasks["tasks"].pop(task_index)
            
            with open("data/todo.json", "w", encoding="utf-8") as f:
                json.dump(tasks, f, ensure_ascii=False, indent=2)
            
            # 只返回列表项的HTML
            return templates.TemplateResponse(
                "partials/task_list.html",
                {"request": request, "tasks": tasks.get("tasks", [])}
            )
    except (FileNotFoundError, json.JSONDecodeError):
        return templates.TemplateResponse(
            "partials/task_list.html",
            {"request": request, "tasks": []}
        )

@app.post("/ai-analysis")
async def ai_analysis():
    try:
        with open("data/memo.html", "r", encoding="utf-8") as f:
            content = f.read()
        
        from .llm_agent import LLMAgent
        agent = LLMAgent()
        tasks = agent.analyze_memo(content)
        agent.save_todo(tasks)
        
        return {"message": "Analysis complete", "tasks": tasks}
    except Exception as e:
        return {"error": str(e)}