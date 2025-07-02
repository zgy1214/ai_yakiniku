import subprocess

import subprocess
import shutil
import os
from pathlib import Path

def separate_audio(input_path,output_dir = './pipeline'):
    try:
        # 调用 demucs 分离
        subprocess.run(["demucs", input_path], check=True)
        print("分离完成，结果在 separated/ 文件夹中")

        # 获取分离输出目录
        input_name = Path(input_path).stem  # 不带扩展名
        model_name = "htdemucs"  # 默认模型名
        vocals_path = Path("separated") / model_name / input_name / "vocals.wav"

        if vocals_path.exists():
            # 创建目标目录
            output_dir = Path(output_dir)
            output_dir.mkdir(exist_ok=True)

            # 移动 vocals.wav 到目标目录
            target_path = output_dir / "vocals.wav"
            shutil.move(str(vocals_path), target_path)
            print(f"人声文件已移动到: {target_path}")

            # 可选：删除分离后其余无用文件
            shutil.rmtree(Path("separated") / model_name / input_name)
        else:
            print("未找到分离后的人声文件")

    except subprocess.CalledProcessError as e:
        print("分离失败：", e)


if __name__ == '__main__':
    separate_audio('./input/#2.aac')
