import { Controller, Post, Get, Body, HttpCode, HttpStatus, Param, UseGuards, Put, Delete } from '@nestjs/common';
import { AdminService, LoginAdminDto, CreateMaeDto, CreateFilhoDto, CreateAdminDto, UpdateMaeDto, UpdateFilhoDto } from './admin.service';
import { MasterAdminGuard } from './guards/master-admin.guard';

@Controller()
export class AdminController {
  constructor(private readonly adminService: AdminService) {}

  @Post('admin/login-master')
  @HttpCode(HttpStatus.OK)
  async loginMasterAdmin(@Body() loginAdminDto: LoginAdminDto) {
    return this.adminService.loginMasterAdmin(loginAdminDto);
  }

  @Post('admin/create-mae')
  @UseGuards(MasterAdminGuard)
  async createMae(@Body() createMaeDto: CreateMaeDto) {
    return this.adminService.createMae(createMaeDto);
  }

  @Post('admin/create-filho')
  @UseGuards(MasterAdminGuard)
  async createFilho(@Body() createFilhoDto: CreateFilhoDto) {
    return this.adminService.createFilho(createFilhoDto);
  }

  @Get('admin/maes')
  @UseGuards(MasterAdminGuard)
  async getAllMaes() {
    return this.adminService.getAllMaes();
  }

  @Get('admin/filhos')
  @UseGuards(MasterAdminGuard)
  async getAllFilhos() {
    return this.adminService.getAllFilhos();
  }

  @Post('admin/create-admin')
  @UseGuards(MasterAdminGuard)
  async createAdmin(@Body() createAdminDto: CreateAdminDto) {
    return this.adminService.createAdmin(createAdminDto);
  }

  @Get('admin/admins')
  @UseGuards(MasterAdminGuard)
  async getAllAdmins() {
    return this.adminService.getAllAdmins();
  }

  @Put('admin/mae/:id')
  @UseGuards(MasterAdminGuard)
  async updateMae(@Param('id') id: string, @Body() updateMaeDto: UpdateMaeDto) {
    return this.adminService.updateMae(id, updateMaeDto);
  }

  @Delete('admin/mae/:id')
  @UseGuards(MasterAdminGuard)
  async deleteMae(@Param('id') id: string) {
    return this.adminService.deleteMae(id);
  }

  @Put('admin/filho/:id')
  @UseGuards(MasterAdminGuard)
  async updateFilho(@Param('id') id: string, @Body() updateFilhoDto: UpdateFilhoDto) {
    return this.adminService.updateFilho(id, updateFilhoDto);
  }

  @Delete('admin/filho/:id')
  @UseGuards(MasterAdminGuard)
  async deleteFilho(@Param('id') id: string) {
    return this.adminService.deleteFilho(id);
  }

  @Get('api/names/:userId/:userType')
  async getNames(
    @Param('userId') userId: string,
    @Param('userType') userType: string,
  ) {
    return this.adminService.getNames(userId, userType);
  }


}