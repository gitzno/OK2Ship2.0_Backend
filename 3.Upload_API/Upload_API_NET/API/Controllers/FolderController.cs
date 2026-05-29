using Core.DTOs;
using Core.Interfaces.IServices;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;

namespace API.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class FolderController : ControllerBase
    {
        private readonly IFolderService _folderService;

        public FolderController(IFolderService folderService)
        {
            _folderService = folderService;
        }

        [HttpPost("get-upload-urls")]
        public async Task<IActionResult> getUploadURLs([FromBody] List<string> fileNames)
        {
            var resonponse = new ServiceResult();

            resonponse = await _folderService.getURLsUploadFileAync(fileNames.ToArray());

            return Ok(resonponse);
        }
    }
}
