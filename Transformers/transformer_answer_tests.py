import torch 
import torch.nn.functional as f
from torch import Tensor 

g_cpu = torch.Generator()
g_cpu.manual_seed(2847587347)

def soft_scaled_dot_product_attention_answer(query: Tensor, key: Tensor, value: Tensor) -> Tensor: 
    temp = query.bmm(key.transpose(1,2))
    scale = key.size(-1) ** 0.5 
    softmax = f.softmax(temp/scale, dim=-1)
    return softmax.bmm(value)

def run_test(
    soft_scaled_dot_product_attention = None, 
): 
    print("---------------------test start---------------------------")

    key = torch.rand(64, 32, 512, generator = g_cpu)
    query = torch.rand(64, 32, 512, generator = g_cpu)
    value = torch.rand(64, 32, 512, generator = g_cpu)

    if soft_scaled_dot_product_attention: 
        test_ans = soft_scaled_dot_product_attention(query, key, value)
        real_ans = soft_scaled_dot_product_attention_answer(query, key, value)

        assert (torch.equal(test_ans, real_ans), "soft scaled dot product attention mismatch")
    
    print("---------------------test end---------------------------")
