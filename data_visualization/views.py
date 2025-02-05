import plotly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
import pandas as pd
import plotly.express as px
import json

class UploadCSV(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        file_obj = request.FILES['file']  # 获取上传的文件
        df = pd.read_csv(file_obj)  # 解析 CSV 数据

        # 判断列数是否足够
        if len(df.columns) < 3:
            return Response({"error": "CSV file must contain at least 3 columns for visualization."}, status=400)

        # 获取列名
        columns = df.columns

        # 图表 1：3D 散点图
        scatter_3d = px.scatter_3d(
            df, x=columns[0], y=columns[1], z=columns[2], color=columns[0],
            title="3D Scatter Plot"
        )

        # 图表 2：气泡图
        bubble_chart = px.scatter(
            df, x=columns[0], y=columns[1], size=columns[2], color=columns[0],
            title="2D Bubble Chart"
        )

        # 将两个图表转为 JSON 格式
        scatter_3d_json = json.dumps(scatter_3d, cls=plotly.utils.PlotlyJSONEncoder)
        bubble_chart_json = json.dumps(bubble_chart, cls=plotly.utils.PlotlyJSONEncoder)

        return Response({
            "scatter_3d": scatter_3d_json,
            "bubble_chart": bubble_chart_json
        })


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
import plotly.express as px
import plotly.io as pio
import json
import os

@csrf_exempt
def generate_chart(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            chart_type = data.get("chartType")
            dataset = data.get("dataset")

            df = pd.DataFrame(dataset)
            chart = None

            if chart_type == "Bar Chart":
                chart = px.bar(df, x=df.columns[0], y=df.columns[1])
            elif chart_type == "Line Chart":
                chart = px.line(df, x=df.columns[0], y=df.columns[1])
            elif chart_type == "Pie Chart":
                chart = px.pie(df, names=df.columns[0], values=df.columns[1])
            # Add more chart types as needed

            return JsonResponse({"chart": chart.to_plotly_json()})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def export_chart(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            chart_type = data.get("chartType")
            dataset = data.get("dataset")

            df = pd.DataFrame(dataset)
            chart = None

            if chart_type == "Bar Chart":
                chart = px.bar(df, x=df.columns[0], y=df.columns[1])
            elif chart_type == "Line Chart":
                chart = px.line(df, x=df.columns[0], y=df.columns[1])
            elif chart_type == "Pie Chart":
                chart = px.pie(df, names=df.columns[0], values=df.columns[1])
            # Add more chart types as needed

            file_path = os.path.join("media", f"{chart_type.replace(' ', '_')}.png")
            pio.write_image(chart, file_path)

            with open(file_path, "rb") as f:
                return JsonResponse({"file": f.read()})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
